#!/usr/bin/env python3
"""Hallway-specific location agent."""
from typing import Dict, List, Optional
import logging

from agents.location_agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)


class HallwayAgent(BaseAgent):
    """Agent with knowledge about hallway environments."""

    def __init__(self, config: Dict):
        super().__init__("hallway_agent", "hallway", config)
        self.hallway_context = {
            "typical_temp_range": (19, 24),
            "typical_humidity_range": (35, 65),
            "high_traffic_hours": [(8, 10), (12, 14), (17, 19)],
            "activities": ["transit", "entry/exit", "waiting", "brief_conversations"],
        }

    def prepare_llm_context(
        self, query: str, sensor_data: Dict, additional_context: Optional[Dict] = None
    ) -> str:
        context = (
            "You are an AI assistant for a building hallway/entrance environment.\n\n"
            "Current Hallway Conditions:\n"
            f"{self._format_sensor_context(sensor_data)}\n\n"
            "Hallway Environment Knowledge:\n"
            "- This is a building entrance/hallway area with regular foot traffic\n"
            f"- Temperature is generally stable: {self.hallway_context['typical_temp_range'][0]}-"
            f"{self.hallway_context['typical_temp_range'][1]}°C\n"
            f"- Humidity varies with outdoor conditions: {self.hallway_context['typical_humidity_range'][0]}-"
            f"{self.hallway_context['typical_humidity_range'][1]}%\n"
            f"- Common activities: {', '.join(self.hallway_context['activities'])}\n"
            "- High traffic periods: 8-10 AM, 12-2 PM, 5-7 PM\n\n"
            "Hallway-Specific Interpretations:\n"
            "- Temperature changes often reflect outdoor weather conditions\n"
            "- Humidity fluctuations typically correlate with outside weather and door openings\n"
            "- Air quality changes might indicate high foot traffic, outdoor air infiltration, or cleaning activities\n"
            "- This area serves as a transition zone between indoor and outdoor environments\n\n"
            f"User Query: {query}\n\n"
            "Please provide a helpful response considering the hallway context and current environmental conditions."
        )
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
            "building_access_monitoring",
        ]

