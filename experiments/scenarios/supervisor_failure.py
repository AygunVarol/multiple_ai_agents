import asyncio
import logging

from agents.supervisor.supervisor_agent import SupervisorAgent
from agents.location_agents.office_agent import OfficeAgent

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    supervisor = SupervisorAgent("config/agent_config.yaml")
    office = OfficeAgent({"port": 8081, "supervisor_endpoint": "http://localhost:8080"})

    await office.start_background_tasks()
    await asyncio.sleep(1)
    # Simulate supervisor failure by not using it after 1 second
    await asyncio.sleep(1)
    await office.shutdown()


if __name__ == "__main__":
    asyncio.run(main())

