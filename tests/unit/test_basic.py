import sys, os
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from sensors.bme680_reader import BME680Reader


def test_mock_reading_sync():
    reader = BME680Reader(mock=True)
    data = asyncio.run(reader.read_async())
    assert "temperature" in data
    assert "humidity" in data

