from __future__ import annotations

import asyncio
import logging
import time
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class TaskAllocator:
    """Allocate tasks based on resource utilization and heartbeats."""

    def __init__(self, threshold: float = 0.7) -> None:
        self.threshold = threshold
        self.agents: Dict[str, Dict] = {}
        self.heartbeats: Dict[str, float] = {}
        self.leader: Optional[str] = None
        self.utilization: float = 0.0

    def update_utilization(self, util: float) -> None:
        self.utilization = util

    async def register(self, agent_id: str, info: Dict) -> None:
        self.agents[agent_id] = info
        self.heartbeats[agent_id] = time.time()
        if self.leader is None or agent_id < self.leader:
            self.leader = agent_id

    def heartbeat(self, agent_id: str) -> None:
        self.heartbeats[agent_id] = time.time()

    def elect_leader(self) -> str:
        now = time.time()
        active = [a for a, t in self.heartbeats.items() if now - t < 10]
        if not active:
            raise RuntimeError("No active agents for leader election")
        self.leader = min(active)
        return self.leader

    def allocate(self) -> Optional[str]:
        if not self.agents:
            return None
        if self.utilization > 0.9:
            return None
        sorted_agents = sorted(self.agents.values(), key=lambda a: a.get("load", 0))
        if sorted_agents and self.utilization > self.threshold:
            return sorted_agents[0]["id"]
        return self.leader

