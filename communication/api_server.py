from __future__ import annotations

import logging
from typing import Iterable

from aiohttp import web

logger = logging.getLogger(__name__)


class APIServer:
    """Lightweight aiohttp server."""

    def __init__(self, routes: Iterable[web.RouteDef] | None = None) -> None:
        self.app = web.Application()
        if routes:
            self.app.add_routes(list(routes))

    def run(self, host: str = "0.0.0.0", port: int = 8000) -> None:
        logger.info("Starting API server on %s:%s", host, port)
        web.run_app(self.app, host=host, port=port)

