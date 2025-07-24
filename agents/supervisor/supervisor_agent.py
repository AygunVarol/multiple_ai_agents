#!/usr/bin/env python3
"""
Supervisor Agent for Multi-Agent LLM Smart Environment
Orchestrates distributed LLM agents with dynamic task allocation
"""

import asyncio
import logging
import time
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional

import httpx
import psutil
import uvicorn
import yaml
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class Agent:
    id: str
    location: str
    endpoint: str
    status: str = "active"
    last_seen: float = 0
    load: float = 0.0
    capabilities: List[str] = None

@dataclass
class Task:
    id: str
    query: str
    location: Optional[str] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    max_latency: float = 5.0
    created_at: float = 0

class TaskAllocator:
    """Dynamic task allocation algorithm"""
    
    def __init__(self, resource_threshold: float = 0.7):
        self.resource_threshold = resource_threshold
        
    def allocate_task(self, task: Task, agents: Dict[str, Agent]) -> Optional[str]:
        """Allocate task to most suitable agent"""
        
        # Filter available agents
        available_agents = {
            id: agent for id, agent in agents.items() 
            if agent.status == "active" and agent.load < self.resource_threshold
        }
        
        if not available_agents:
            return None
            
        # Location-specific task
        if task.location:
            location_agents = {
                id: agent for id, agent in available_agents.items()
                if agent.location == task.location
            }
            if location_agents:
                # Select least loaded agent for the location
                return min(location_agents.items(), key=lambda x: x[1].load)[0]
        
        # General task - select least loaded agent
        return min(available_agents.items(), key=lambda x: x[1].load)[0]

class SupervisorAgent:
    def __init__(self, config_path: str):
        self.config = self.load_config(config_path)
        self.agents: Dict[str, Agent] = {}
        self.task_queue: List[Task] = []
        self.task_allocator = TaskAllocator(
            resource_threshold=self.config.get('resource_threshold', 0.7)
        )
        self.app = FastAPI(title="Supervisor Agent API")
        self.setup_routes()
        
    def load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file"""
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    
    def setup_routes(self):
        """Setup FastAPI routes"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        @self.app.get("/agents")
        async def list_agents():
            return {"agents": list(self.agents.values())}
        
        @self.app.post("/register")
        async def register_agent(agent_data: dict):
            agent = Agent(**agent_data)
            agent.last_seen = time.time()
            self.agents[agent.id] = agent
            logger.info(f"Registered agent: {agent.id} at {agent.location}")
            return {"status": "registered", "agent_id": agent.id}
        
        @self.app.post("/task")
        async def submit_task(task_data: dict):
            task = Task(
                id=f"task_{int(time.time() * 1000)}",
                created_at=time.time(),
                **task_data
            )
            
            # Try to allocate immediately
            agent_id = self.task_allocator.allocate_task(task, self.agents)
            
            if agent_id:
                result = await self.execute_task(agent_id, task)
                return {"status": "completed", "result": result, "agent": agent_id}
            else:
                # Check if we should offload to cloud
                if await self.should_offload_to_cloud():
                    result = await self.execute_cloud_task(task)
                    return {"status": "completed", "result": result, "agent": "cloud"}
                else:
                    self.task_queue.append(task)
                    return {"status": "queued", "task_id": task.id}
        
        @self.app.get("/status")
        async def get_status():
            system_stats = {
                "cpu_percent": psutil.cpu_percent(),
                "memory_percent": psutil.virtual_memory().percent,
                "active_agents": len([a for a in self.agents.values() if a.status == "active"]),
                "queued_tasks": len(self.task_queue),
                "uptime": time.time() - self.start_time
            }
            return system_stats
    
    async def execute_task(self, agent_id: str, task: Task) -> dict:
        """Execute task on specified agent"""
        agent = self.agents[agent_id]
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{agent.endpoint}/execute",
                    json={
                        "query": task.query,
                        "location": task.location,
                        "task_id": task.id
                    },
                    timeout=task.max_latency
                )
                response.raise_for_status()
                
                # Update agent load (simplified)
                agent.load = min(agent.load + 0.1, 1.0)
                
                return response.json()
                
        except Exception as e:
            logger.error(f"Task execution failed on agent {agent_id}: {e}")
            agent.status = "error"
            raise HTTPException(status_code=500, detail=str(e))
    
    async def should_offload_to_cloud(self) -> bool:
        """Determine if tasks should be offloaded to cloud"""
        system_load = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent
        
        return (system_load > 70 or memory_usage > 80 or 
                len([a for a in self.agents.values() if a.status == "active"]) == 0)
    
    async def execute_cloud_task(self, task: Task) -> dict:
        """Execute task on cloud infrastructure"""
        # Placeholder for cloud execution logic
        logger.info(f"Executing task {task.id} on cloud")
        
        # Simulate cloud API call
        await asyncio.sleep(0.5)  # Simulate network latency
        
        return {
            "response": f"Cloud processing complete for: {task.query}",
            "execution_time": 0.5,
            "source": "cloud"
        }
    
    async def monitor_agents(self):
        """Monitor agent health and update status"""
        while True:
            current_time = time.time()
            
            for agent_id, agent in self.agents.items():
                if current_time - agent.last_seen > 30:  # 30 second timeout
                    agent.status = "inactive"
                    logger.warning(f"Agent {agent_id} marked as inactive")
                
                # Gradually reduce load over time
                agent.load = max(agent.load - 0.01, 0.0)
            
            await asyncio.sleep(10)  # Check every 10 seconds
    
    async def process_task_queue(self):
        """Process queued tasks"""
        while True:
            if self.task_queue:
                task = self.task_queue.pop(0)
                agent_id = self.task_allocator.allocate_task(task, self.agents)
                
                if agent_id:
                    try:
                        await self.execute_task(agent_id, task)
                        logger.info(f"Processed queued task {task.id} on agent {agent_id}")
                    except Exception as e:
                        logger.error(f"Failed to process queued task {task.id}: {e}")
                        # Re-queue if not expired
                        if time.time() - task.created_at < 300:  # 5 minute timeout
                            self.task_queue.append(task)
                else:
                    # Re-queue if no agents available
                    self.task_queue.append(task)
            
            await asyncio.sleep(1)
    
    async def start_background_tasks(self):
        """Start background monitoring tasks"""
        self.start_time = time.time()
        asyncio.create_task(self.monitor_agents())
        asyncio.create_task(self.process_task_queue())
    
    def run(self, host: str = "0.0.0.0", port: int = 8080):
        """Run the supervisor agent"""
        logger.info(f"Starting Supervisor Agent on {host}:{port}")
        
        # Start background tasks
        asyncio.create_task(self.start_background_tasks())
        
        uvicorn.run(
            self.app,
            host=host,
            port=port,
            log_level="info"
        )

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Multi-Agent LLM Supervisor")
    parser.add_argument("--config", default="config/agent_config.yaml", 
                       help="Configuration file path")
    parser.add_argument("--host", default="0.0.0.0", help="Host address")
    parser.add_argument("--port", type=int, default=8080, help="Port number")
    
    args = parser.parse_args()
    
    supervisor = SupervisorAgent(args.config)
    supervisor.run(host=args.host, port=args.port)