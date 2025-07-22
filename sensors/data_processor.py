from __future__ import annotations

import statistics
from typing import Dict, List


class DataProcessor:
    """Utility for maintaining a buffer of sensor readings and computing stats."""

    def __init__(self, maxlen: int = 100) -> None:
        self.maxlen = maxlen
        self.buffer: List[Dict[str, float]] = []

    def add_reading(self, reading: Dict[str, float]) -> None:
        self.buffer.append(reading)
        if len(self.buffer) > self.maxlen:
            self.buffer = self.buffer[-self.maxlen :]

    def average(self) -> Dict[str, float]:
        if not self.buffer:
            return {}
        keys = self.buffer[0].keys()
        return {k: statistics.mean(r[k] for r in self.buffer) for k in keys}

