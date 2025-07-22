import asyncio
import logging
from typing import Any, Dict

import psutil

logger = logging.getLogger(__name__)


class ResourceMonitor:
    """Periodically sample system resource usage and publish via queue."""

    def __init__(self, queue: asyncio.Queue, interval: float = 5.0) -> None:
        self.queue = queue
        self.interval = interval
        self._task: asyncio.Task | None = None
        self.running = False

    async def start(self) -> None:
        if not self.running:
            self.running = True
            self._task = asyncio.create_task(self._run())

    async def _run(self) -> None:
        while self.running:
            metrics: Dict[str, Any] = {
                "cpu": psutil.cpu_percent(),
                "memory": psutil.virtual_memory().percent,
            }
            await self.queue.put(metrics)
            await asyncio.sleep(self.interval)

    async def stop(self) -> None:
        self.running = False
        if self._task:
            await self._task

