#!/usr/bin/env python3
"""Office-specific location agent."""
from typing import Dict, List, Optional
import logging

from agents.location_agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)


class OfficeAgent(BaseAgent):
    """Agent with knowledge about office environments."""

    def __init__(self, config: Dict):
        super().__init__("office_agent", "office", config)
        self.office_context = {
            "typical_temp_range": (20, 25),
            "typical_humidity_range": (40, 60),
            "work_hours": (8, 18),
            "activities": ["working", "meetings", "computer_use", "printing"],
        }

    def prepare_llm_context(
        self, query: str, sensor_data: Dict, additional_context: Optional[Dict] = None
    ) -> str:
        context = (
            "You are an AI assistant for an office environment.\n\n"
            "Current Office Conditions:\n"
            f"{self._format_sensor_context(sensor_data)}\n\n"
            "Office Environment Knowledge:\n"
            f"- This is a typical office workspace with computers, printers, and meeting areas\n"
            f"- Normal temperature range: {self.office_context['typical_temp_range'][0]}-"
            f"{self.office_context['typical_temp_range'][1]}°C\n"
            f"- Ideal humidity: {self.office_context['typical_humidity_range'][0]}-"
            f"{self.office_context['typical_humidity_range'][1]}%\n"
            f"- Common activities: {', '.join(self.office_context['activities'])}\n"
            f"- Work hours: {self.office_context['work_hours'][0]}:00 - {self.office_context['work_hours'][1]}:00\n\n"
            "Office-Specific Interpretations:\n"
            "- High humidity might indicate poor ventilation or many people present\n"
            "- Temperature spikes could be from computers/equipment or external heat\n"
            "- Air quality changes might be from printer toner, cleaning products, or occupancy\n"
            "- Pressure changes are typically weather-related\n\n"
            f"User Query: {query}\n\n"
            "Please provide a helpful response considering the office context and current environmental conditions."
        )
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
            "temperature_control_advice",
        ]

