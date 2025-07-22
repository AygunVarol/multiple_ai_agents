from __future__ import annotations

import logging
from typing import Any, Dict

import httpx

logger = logging.getLogger(__name__)


class MessageHandler:
    """Simple HTTP-based message sender."""

    async def post(self, url: str, data: Dict[str, Any], timeout: float = 5.0) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post(url, json=data)
            resp.raise_for_status()
            return resp.json()

