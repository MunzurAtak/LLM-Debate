import requests

from .base import BaseLLM, GenerationConfig, Message


class OllamaLLM(BaseLLM):
    """LLM backend that calls a locally running Ollama instance.

    Ollama exposes a REST API and handles AMD/NVIDIA GPU routing
    transparently. No CUDA required.

    Args:
        model: Ollama model tag, e.g. "llama3.2:3b" or "qwen2.5:7b".
        host: Base URL of the Ollama server.
    """

    def __init__(
        self,
        model: str,
        host: str = "http://localhost:11434",
    ) -> None:
        self._model = model
        self._host = host.rstrip("/")

    @property
    def model_name(self) -> str:
        return self._model

    def generate(self, messages: list[Message], config: GenerationConfig) -> str:
        # Build the options dict that Ollama accepts.
        # temperature controls randomness (0 = deterministic, 1 = creative).
        # num_predict is Ollama's name for max output tokens.
        options: dict = {
            "temperature": config.temperature,
            "num_predict": config.max_tokens,
        }

        # Only include seed if explicitly set — Ollama uses it for
        # reproducible sampling. Without it, outputs will vary each run.
        if config.seed is not None:
            options["seed"] = config.seed

        # Ollama's /api/chat endpoint accepts a messages array
        # in the standard OpenAI chat format: [{"role": ..., "content": ...}]
        payload = {
            "model": self._model,
            "messages": [m.to_dict() for m in messages],
            "stream": False,   # We want the full response at once, not streamed
            "options": options,
        }

        response = requests.post(
            f"{self._host}/api/chat",
            json=payload,
            timeout=120,  # 2-minute timeout — local models can be slow
        )
        # Raise an exception if the server returned 4xx or 5xx
        response.raise_for_status()

        # The response JSON has the shape: {"message": {"role": "assistant", "content": "..."}}
        return response.json()["message"]["content"].strip()
