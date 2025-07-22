#!/usr/bin/env python3
"""
Base Location Agent for Multi-Agent LLM Smart Environment
Handles sensor data collection, local LLM inference, and communication
"""

import asyncio
import logging
import time
import json
import httpx
import psutil
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from sensors.bme680_reader import BME680Reader
from models.llama_wrapper import LlamaWrapper

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SensorReading:
    timestamp: float
    temperature: float
    humidity: float
    pressure: float
    gas_resistance: float
    air_quality_index: float

@dataclass
class TaskRequest:
    task_id: str
    query: str
    location: str
    priority: int = 2
    max_latency: float = 5.0
    context: Optional[Dict] = None

class BaseAgent(ABC):
    def __init__(self, agent_id: str, location: str, config: Dict):
        self.agent_id = agent_id
        self.location = location
        self.config = config
        
        # Initialize components
        self.sensor_reader = BME680Reader(config.get('sensor_port', '/dev/i2c-1'))
        self.llm_model = LlamaWrapper(config.get('model', 'llama-3.2-1b'))
        
        # State management
        self.sensor_data: List[SensorReading] = []
        self.status = "active"
        self.load = 0.0
        self.last_heartbeat = time.time()
        
        # Supervisor connection
        self.supervisor_endpoint = config.get('supervisor_endpoint', 'http://192.168.1.100:8080')
        
        # FastAPI setup
        self.app = FastAPI(title=f"{location.title()} Agent API")
        self.setup_routes()
        
        # Background tasks
        self.running = False
    
    def setup_routes(self):
        """Setup FastAPI routes for agent communication"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        @self.app.get("/health")
        async def health_check():
            return {
                "agent_id": self.agent_id,
                "location": self.location,
                "status": self.status,
                "load": self.load,
                "last_reading": len(self.sensor_data),
                "uptime": time.time() - self.last_heartbeat
            }
        
        @self.app.get("/sensor_data")
        async def get_sensor_data(limit: int = 100):
            return {
                "location": self.location,
                "readings": self.sensor_data[-limit:],
                "count": len(self.sensor_data)
            }
        
        @self.app.post("/execute")
        async def execute_task(task: dict):
            try:
                task_request = TaskRequest(**task)
                result = await self.process_task(task_request)
                return {
                    "task_id": task_request.task_id,
                    "result": result,
                    "agent": self.agent_id,
                    "location": self.location,
                    "execution_time": time.time()
                }
            except Exception as e:
                logger.error(f"Task execution failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))
    
    async def process_task(self, task: TaskRequest) -> Dict:
        """Process incoming task using local LLM with sensor context"""
        self.load = min(self.load + 0.1, 1.0)
        
        try:
            # Get recent sensor data for context
            recent_data = self.get_recent_sensor_context()
            
            # Prepare context for LLM
            context = self.prepare_llm_context(task.query, recent_data, task.context)
            
            # Generate response using location-specific knowledge
            response = await self.generate_response(context)
            
            # Update load
            self.load = max(self.load - 0.05, 0.0)
            
            return {
                "response": response,
                "sensor_context": recent_data,
                "location": self.location,
                "timestamp": time.time()
            }
            
        except Exception as e:
            self.load = max(self.load - 0.05, 0.0)
            raise e
    
    def get_recent_sensor_context(self, minutes: int = 10) -> Dict:
        """Get recent sensor readings for context"""
        cutoff_time = time.time() - (minutes * 60)
        recent_readings = [r for r in self.sensor_data if r.timestamp > cutoff_time]
        
        if not recent_readings:
            return {"status": "no_recent_data"}
        
        # Calculate averages for recent period
        avg_temp = sum(r.temperature for r in recent_readings) / len(recent_readings)
        avg_humidity = sum(r.humidity for r in recent_readings) / len(recent_readings)
        avg_pressure = sum(r.pressure for r in recent_readings) / len(recent_readings)
        avg_aqi = sum(r.air_quality_index for r in recent_readings) / len(recent_readings)
        
        return {
            "location": self.location,
            "time_range_minutes": minutes,
            "sample_count": len(recent_readings),
            "averages": {
                "temperature": round(avg_temp, 1),
                "humidity": round(avg_humidity, 1),
                "pressure": round(avg_pressure, 1),
                "air_quality_index": round(avg_aqi, 1)
            },
            "latest_reading": {
                "temperature": recent_readings[-1].temperature,
                "humidity": recent_readings[-1].humidity,
                "pressure": recent_readings[-1].pressure,
                "air_quality_index": recent_readings[-1].air_quality_index,
                "timestamp": recent_readings[-1].timestamp
            }
        }
    
    @abstractmethod
    def prepare_llm_context(self, query: str, sensor_data: Dict, additional_context: Optional[Dict] = None) -> str:
        """Prepare location-specific context for LLM inference"""
        pass
    
    async def generate_response(self, context: str) -> str:
        """Generate response using local LLM"""
        try:
            response = await self.llm_model.generate_async(context)
            return response
        except Exception as e:
            logger.error(f"LLM inference failed: {e}")
            return f"I'm experiencing technical difficulties. Error: {str(e)}"
    
    async def collect_sensor_data(self):
        """Background task to collect sensor data"""
        while self.running:
            try:
                reading = await self.sensor_reader.read_async()
                if reading:
                    # Add AQI calculation based on gas resistance
                    aqi = self.calculate_air_quality_index(reading['gas_resistance'])
                    
                    sensor_reading = SensorReading(
                        timestamp=time.time(),
                        temperature=reading['temperature'],
                        humidity=reading['humidity'],
                        pressure=reading['pressure'],
                        gas_resistance=reading['gas_resistance'],
                        air_quality_index=aqi
                    )
                    
                    self.sensor_data.append(sensor_reading)
                    
                    # Keep only last 1000 readings to manage memory
                    if len(self.sensor_data) > 1000:
                        self.sensor_data = self.sensor_data[-1000:]
                        
                    logger.debug(f"Collected sensor data: T={reading['temperature']}°C, "
                               f"H={reading['humidity']}%, AQI={aqi}")
                    
            except Exception as e:
                logger.error(f"Sensor data collection failed: {e}")
            
            await asyncio.sleep(1)  # Collect data every second
    
    def calculate_air_quality_index(self, gas_resistance: float) -> float:
        """Calculate AQI from gas resistance (simplified calculation)"""
        # This is a simplified AQI calculation
        # In production, you'd use proper calibration curves
        if gas_resistance > 50000:
            return 1.0  # Excellent
        elif gas_resistance > 20000:
            return 2.0  # Good
        elif gas_resistance > 10000:
            return 3.0  # Moderate
        elif gas_resistance > 5000:
            return 4.0  # Poor
        else:
            return 5.0  # Very Poor

    def _format_sensor_context(self, sensor_data: Dict) -> str:
        """Format sensor data for LLM context."""
        if sensor_data.get("status") == "no_recent_data":
            return "No recent sensor data available."

        latest = sensor_data.get("latest_reading", {})
        averages = sensor_data.get("averages", {})

        context = (
            f"Recent Sensor Data (last {sensor_data.get('time_range_minutes', 10)} minutes):\n"
            f"- Current Temperature: {latest.get('temperature', 'N/A')}°C\n"
            f"- Current Humidity: {latest.get('humidity', 'N/A')}%\n"
            f"- Current Pressure: {latest.get('pressure', 'N/A')} hPa\n"
            f"- Current Air Quality Index: {latest.get('air_quality_index', 'N/A')}\n\n"
            "Average Conditions:\n"
            f"- Avg Temperature: {averages.get('temperature', 'N/A')}°C\n"
            f"- Avg Humidity: {averages.get('humidity', 'N/A')}%\n"
            f"- Avg Pressure: {averages.get('pressure', 'N/A')} hPa\n"
            f"- Avg Air Quality: {averages.get('air_quality_index', 'N/A')}\n\n"
            f"Data points: {sensor_data.get('sample_count', 0)} readings"
        )

        return context
    
    async def register_with_supervisor(self):
        """Register this agent with the supervisor"""
        registration_data = {
            "id": self.agent_id,
            "location": self.location,
            "endpoint": f"http://localhost:{self.config.get('port', 8081)}",
            "capabilities": self.get_capabilities()
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.supervisor_endpoint}/register",
                    json=registration_data,
                    timeout=10.0
                )
                response.raise_for_status()
                logger.info(f"Successfully registered with supervisor: {response.json()}")
                
        except Exception as e:
            logger.error(f"Failed to register with supervisor: {e}")
    
    async def send_heartbeat(self):
        """Send periodic heartbeat to supervisor"""
        while self.running:
            try:
                async with httpx.AsyncClient() as client:
                    heartbeat_data = {
                        "agent_id": self.agent_id,
                        "status": self.status,
                        "load": self.load,
                        "timestamp": time.time()
                    }
                    
                    await client.post(
                        f"{self.supervisor_endpoint}/heartbeat",
                        json=heartbeat_data,
                        timeout=5.0
                    )
                    
                self.last_heartbeat = time.time()
                
            except Exception as e:
                logger.warning(f"Heartbeat failed: {e}")
            
            await asyncio.sleep(30)  # Send heartbeat every 30 seconds
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Return list of agent capabilities"""
        pass
    
    async def start_background_tasks(self):
        """Start background tasks"""
        self.running = True
        
        # Start background tasks
        asyncio.create_task(self.collect_sensor_data())
        asyncio.create_task(self.send_heartbeat())
        
        # Register with supervisor
        await self.register_with_supervisor()
    
    async def shutdown(self):
        """Graceful shutdown"""
        logger.info(f"Shutting down {self.agent_id}")
        self.running = False
        
        # Close sensor connection
        if hasattr(self.sensor_reader, 'close'):
            self.sensor_reader.close()
    
    def run(self, host: str = "0.0.0.0", port: int = 8081):
        """Run the agent server"""
        logger.info(f"Starting {self.location} agent on {host}:{port}")
        
        # Start background tasks
        asyncio.create_task(self.start_background_tasks())
        
        uvicorn.run(
            self.app,
            host=host,
            port=port,
            log_level="info"
        )
