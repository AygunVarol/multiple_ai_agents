import asyncio
import logging

from agents.supervisor.supervisor_agent import SupervisorAgent

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    supervisor = SupervisorAgent("config/agent_config.yaml")
    # Simulate high load
    await asyncio.sleep(1)
    # Normally would trigger offload logic


if __name__ == "__main__":
    asyncio.run(main())

