import pytest
import asyncio
import tempfile
import os
from unittest.mock import MagicMock
from agents.supervisor.supervisor_agent import SupervisorAgent
from agents.location_agents.base_agent import BaseLocationAgent

@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def temp_config_dir():
    """Create temporary configuration directory"""
    with tempfile.TemporaryDirectory() as temp_dir:
        config_dir = os.path.join(temp_dir, "config")
        os.makedirs(config_dir)
        yield config_dir

@pytest.fixture
def mock_sensor():
    """Mock BME680 sensor"""
    sensor = MagicMock()
    sensor.temperature = 22.5
    sensor.humidity = 45.0
    sensor.pressure = 1013.25
    sensor.gas = 50000
    return sensor

@pytest.fixture
def sample_agent_config():
    """Sample agent configuration"""
    return {
        "id": "test_agent",
        "location": "test_room",
        "host": "localhost",
        "port": 8080,
        "sensor": {
            "type": "bme680",
            "port": "/dev/ttyUSB0"
        },
        "model": {
            "name": "llama-3.2-1b",
            "specialization": "test_environment"
        }
    }

@pytest.fixture
async def supervisor_agent(temp_config_dir):
    """Create supervisor agent instance"""
    config = {
        "host": "localhost",
        "port": 8080,
        "model": {"name": "llama-3.2-1b"},
        "resource_monitoring": {
            "cpu_threshold": 0.8,
            "memory_threshold": 0.85,
            "check_interval": 30
        }
    }
    agent = SupervisorAgent(config)
    await agent.initialize()
    yield agent
    await agent.shutdown()
