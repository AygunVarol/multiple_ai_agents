#!/usr/bin/env python3
"""Kitchen-specific location agent."""
from typing import Dict, List, Optional
import logging

from agents.location_agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)


class KitchenAgent(BaseAgent):
    """Agent with knowledge about kitchen environments."""

    def __init__(self, config: Dict):
        super().__init__("kitchen_agent", "kitchen", config)
        self.kitchen_context = {
            "typical_temp_range": (18, 28),
            "typical_humidity_range": (45, 80),
            "cooking_hours": [(7, 9), (12, 14), (18, 21)],
            "activities": ["cooking", "food_storage", "dishwashing", "meal_prep"],
        }

    def prepare_llm_context(
        self, query: str, sensor_data: Dict, additional_context: Optional[Dict] = None
    ) -> str:
        context = (
            "You are an AI assistant for a kitchen environment.\n\n"
            "Current Kitchen Conditions:\n"
            f"{self._format_sensor_context(sensor_data)}\n\n"
            "Kitchen Environment Knowledge:\n"
            "- This is a departmental kitchen used for food preparation and storage\n"
            f"- Temperature range varies more due to cooking: {self.kitchen_context['typical_temp_range'][0]}-"
            f"{self.kitchen_context['typical_temp_range'][1]}°C\n"
            f"- Humidity can be higher during cooking: {self.kitchen_context['typical_humidity_range'][0]}-"
            f"{self.kitchen_context['typical_humidity_range'][1]}%\n"
            f"- Common activities: {', '.join(self.kitchen_context['activities'])}\n"
            "- Typical meal preparation times: 7-9 AM, 12-2 PM, 6-9 PM\n\n"
            "Kitchen-Specific Interpretations:\n"
            "- High humidity is normal during cooking, dishwashing, or when hot food is present\n"
            "- Temperature spikes indicate active cooking or oven/microwave use\n"
            "- Air quality changes might be from cooking odors, food preparation, or gas appliances\n"
            "- Gas resistance changes often indicate cooking activities or food aromas\n\n"
            f"User Query: {query}\n\n"
            "Please provide a helpful response considering the kitchen context and current environmental conditions."
        )
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
            "humidity_management",
        ]

