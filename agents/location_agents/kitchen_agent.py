#!/usr/bin/env python3
"""
Location-Specific Agent Implementations
Office, Kitchen, and Hallway agents with specialized knowledge
"""

from agents.location_agents.base_agent import BaseAgent
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class OfficeAgent(BaseAgent):
    def __init__(self, config: Dict):
        super().__init__("office_agent", "office", config)
        
        # Office-specific knowledge
        self.office_context = {
            "typical_temp_range": (20, 25),  # °C
            "typical_humidity_range": (40, 60),  # %
            "work_hours": (8, 18),  # 24h format
            "activities": ["working", "meetings", "computer_use", "printing"]
        }
    
    def prepare_llm_context(self, query: str, sensor_data: Dict, additional_context: Optional[Dict] = None) -> str:
        """Prepare office-specific context for LLM"""
        context = f"""You are an AI assistant for an office environment. 

Current Office Conditions:
{self._format_sensor_context(sensor_data)}

Office Environment Knowledge:
- This is a typical office workspace with computers, printers, and meeting areas
- Normal temperature range: {self.office_context['typical_temp_range'][0]}-{self.office_context['typical_temp_range'][1]}°C
- Ideal humidity: {self.office_context['typical_humidity_range'][0]}-{self.office_context['typical_humidity_range'][1]}%
- Common activities: {', '.join(self.office_context['activities'])}
- Work hours: {self.office_context['work_hours'][0]}:00 - {self.office_context['work_hours'][1]}:00

Office-Specific Interpretations:
- High humidity might indicate poor ventilation or many people present
- Temperature spikes could be from computers/equipment or external heat
- Air quality changes might be from printer toner, cleaning products, or occupancy
- Pressure changes are typically weather-related

User Query: {query}

Please provide a helpful response considering the office context and current environmental conditions."""
        
        if additional_context:
            context += f"\n\nAdditional Context: {additional_context}"
        
        return context
    
    def get_capabilities(self) -> List[str]:
        return [
            "office_monitoring",
            "workspace_optimization", 
            "equipment_monitoring",
            "air_quality_analysis",
            "occupancy_detection",
            "temperature_control_advice"
        ]

class KitchenAgent(BaseAgent):
    def __init__(self, config: Dict):
        super().__init__("kitchen_agent", "kitchen", config)
        
        # Kitchen-specific knowledge
        self.kitchen_context = {
            "typical_temp_range": (18, 28),  # °C (wider due to cooking)
            "typical_humidity_range": (45, 80),  # % (higher due to cooking)
            "cooking_hours": [(7, 9), (12, 14), (18, 21)],  # Typical meal times
            "activities": ["cooking", "food_storage", "dishwashing", "meal_prep"]
        }
    
    def prepare_llm_context(self, query: str, sensor_data: Dict, additional_context: Optional[Dict] = None) -> str:
        """Prepare kitchen-specific context for LLM"""
        context = f"""You are an AI assistant for a kitchen environment.

Current Kitchen Conditions:
{self._format_sensor_context(sensor_data)}

Kitchen Environment Knowledge:
- This is a departmental kitchen used for food preparation and storage
- Temperature range varies more due to cooking: {self.kitchen_context['typical_temp_range'][0]}-{self.kitchen_context['typical_temp_range'][1]}°C
- Humidity can be higher during cooking: {self.kitchen_context['typical_humidity_range'][0]}-{self.kitchen_context['typical_humidity_range'][1]}%
- Common activities: {', '.join(self.kitchen_context['activities'])}
- Typical meal preparation times: 7-9 AM, 12-2 PM, 6-9 PM

Kitchen-Specific Interpretations:
- High humidity is normal during cooking, dishwashing, or when hot food is present
- Temperature spikes indicate active cooking or oven/microwave use
- Air quality changes might be from cooking odors, food preparation, or gas appliances
- Gas resistance changes often indicate cooking activities or food aromas

User Query: {query}

Please provide a helpful response considering the kitchen context and current environmental conditions."""
        
        if additional_context:
            context += f"\n\nAdditional Context: {additional_context}"
        
        return context
    
    def get_capabilities(self) -> List[str]:
        return [
            "kitchen_monitoring",
            "cooking_activity_detection",
            "food_safety_monitoring",
            "ventilation_analysis",
            "appliance_usage_detection",
            "humidity_management"
        ]

class HallwayAgent(BaseAgent):
    def __init__(self, config: Dict):
        super().__init__("hallway_agent", "hallway", config)
        
        # Hallway-specific knowledge
        self.hallway_context = {
            "typical_temp_range": (19, 24),  # °C
            "typical_humidity_range": (35, 65),  # %
            "high_traffic_hours": [(8, 10), (12, 14), (17, 19)],
            "activities": ["transit", "entry/exit", "waiting", "brief_conversations"]
        }
    
    def prepare_llm_context(self, query: str, sensor_data: Dict, additional_context: Optional[Dict] = None) -> str:
        """Prepare hallway-specific context for LLM"""
        context = f"""You are an AI assistant for a building hallway/entrance environment.

Current Hallway Conditions:
{self._format_sensor_context(sensor_data)}

Hallway Environment Knowledge:
- This is a building entrance/hallway area with regular foot traffic
- Temperature is generally stable: {self.hallway_context['typical_temp_range'][0]}-{self.hallway_context['typical_temp_range'][1]}°C
- Humidity varies with outdoor conditions: {self.hallway_context['typical_humidity_range'][0]}-{self.hallway_context['typical_humidity_range'][1]}%
- Common activities: {', '.join(self.hallway_context['activities'])}
- High traffic periods: 8-10 AM, 12-2 PM, 5-7 PM

Hallway-Specific Interpretations:
- Temperature changes often reflect outdoor weather conditions
- Humidity fluctuations typically correlate with outside weather and door openings
- Air quality changes might indicate high foot traffic, outdoor air infiltration, or cleaning activities
- This area serves as a transition zone between indoor and outdoor environments

User Query: {query}

Please provide a helpful response considering the hallway context and current environmental conditions."""
        
        if additional_context:
            context += f"\n\nAdditional Context: {additional_context}"
        
        return context
    
    def get_capabilities(self) -> List[str]:
        return [
            "entrance_monitoring",
            "traffic_flow_analysis",
            "outdoor_correlation",
            "security_assistance",
            "environmental_transition_tracking",
            "building_access_monitoring"
        ]

# Base class extension for common sensor formatting
def _format_sensor_context(self, sensor_data: Dict) -> str:
    """Format sensor data for LLM context"""
    if sensor_data.get("status") == "no_recent_data":
        return "No recent sensor data available."
    
    latest = sensor_data.get("latest_reading", {})
    averages = sensor_data.get("averages", {})
    
    context = f"""Recent Sensor Data (last {sensor_data.get('time_range_minutes', 10)} minutes):
- Current Temperature: {latest.get('temperature', 'N/A')}°C
- Current Humidity: {latest.get('humidity', 'N/A')}%
- Current Pressure: {latest.get('pressure', 'N/A')} hPa
- Current Air Quality Index: {latest.get('air_quality_index', 'N/A')}

Average Conditions:
- Avg Temperature: {averages.get('temperature', 'N/A')}°C
- Avg Humidity: {averages.get('humidity', 'N/A')}%
- Avg Pressure: {averages.get('pressure', 'N/A')} hPa
- Avg Air Quality: {averages.get('air_quality_index', 'N/A')}

Data points: {sensor_data.get('sample_count', 0)} readings"""
    
    return context

# Monkey patch the method to the base class
BaseAgent._format_sensor_context = _format_sensor_context