import asyncio
import random
from typing import Dict


class BME680Reader:
    """Async wrapper for BME680 sensor with optional mock mode."""

    def __init__(self, port: str = "/dev/i2c-1", mock: bool = True) -> None:
        self.port = port
        self.mock = mock
        self._sensor = None
        if not mock:
            try:
                import bme680  # type: ignore

                self._sensor = bme680.BME680(i2c_addr=0x76)
            except Exception:
                self.mock = True

    async def read_async(self) -> Dict[str, float]:
        if self.mock or not self._sensor:
            await asyncio.sleep(0)
            return {
                "temperature": random.uniform(20, 26),
                "humidity": random.uniform(30, 60),
                "pressure": random.uniform(990, 1020),
                "gas_resistance": random.uniform(5000, 60000),
            }

        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._read_sensor)

    def _read_sensor(self) -> Dict[str, float]:
        self._sensor.get_sensor_data()
        data = self._sensor.data
        return {
            "temperature": data.temperature,
            "humidity": data.humidity,
            "pressure": data.pressure,
            "gas_resistance": data.gas_resistance,
        }

    def close(self) -> None:
        """Close the sensor if needed."""
        self._sensor = None

