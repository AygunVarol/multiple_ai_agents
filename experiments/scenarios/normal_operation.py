import asyncio
import logging

from agents.supervisor.supervisor_agent import SupervisorAgent
from agents.location_agents.office_agent import OfficeAgent
from agents.location_agents.kitchen_agent import KitchenAgent
from agents.location_agents.hallway_agent import HallwayAgent

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    supervisor = SupervisorAgent("config/agent_config.yaml")
    office = OfficeAgent({"port": 8081, "supervisor_endpoint": "http://localhost:8080"})
    kitchen = KitchenAgent({"port": 8082, "supervisor_endpoint": "http://localhost:8080"})
    hallway = HallwayAgent({"port": 8083, "supervisor_endpoint": "http://localhost:8080"})

    await office.start_background_tasks()
    await kitchen.start_background_tasks()
    await hallway.start_background_tasks()

    await asyncio.sleep(2)

    await office.shutdown()
    await kitchen.shutdown()
    await hallway.shutdown()


if __name__ == "__main__":
    asyncio.run(main())

