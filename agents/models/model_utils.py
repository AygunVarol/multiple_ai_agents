from __future__ import annotations

import asyncio
from typing import Any, Callable


async def run_sync(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    """Run a blocking function asynchronously."""

    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: func(*args, **kwargs))

