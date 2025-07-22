import asyncio
from typing import Any
import logging

logger = logging.getLogger(__name__)


class LlamaWrapper:
    """Simplified wrapper around a local or remote LLM model."""

    def __init__(self, model_name: str, use_mock: bool = True) -> None:
        self.model_name = model_name
        self.use_mock = use_mock
        self._model: Any | None = None
        if not use_mock:
            try:
                from ctransformers import AutoModelForCausalLM  # type: ignore

                self._model = AutoModelForCausalLM.from_pretrained(model_name)
            except Exception as exc:
                logger.warning("Falling back to mock model due to: %s", exc)
                self.use_mock = True

    async def generate_async(self, prompt: str, **kwargs: Any) -> str:
        if self.use_mock or not self._model:
            await asyncio.sleep(0)
            return f"Mock response to: {prompt[:50]}"

        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._model, prompt, **kwargs)

