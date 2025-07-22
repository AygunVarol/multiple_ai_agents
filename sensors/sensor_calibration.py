from typing import Dict


class SensorCalibrator:
    """Simple sensor calibration applying constant offsets."""

    def __init__(self, temp_offset: float = 0.0, humidity_offset: float = 0.0) -> None:
        self.temp_offset = temp_offset
        self.humidity_offset = humidity_offset

    def calibrate(self, reading: Dict[str, float]) -> Dict[str, float]:
        reading = dict(reading)
        if "temperature" in reading:
            reading["temperature"] += self.temp_offset
        if "humidity" in reading:
            reading["humidity"] += self.humidity_offset
        return reading

