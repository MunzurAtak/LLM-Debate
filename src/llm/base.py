from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class Message:
    """A single message in a conversation."""
    role: str  # "system" | "user" | "assistant"
    content: str

    def to_dict(self) -> dict:
        return {"role": self.role, "content": self.content}


@dataclass
class GenerationConfig:
    """Parameters that control how the LLM generates a response."""
    temperature: float = 0.7
    max_tokens: int = 512
    seed: Optional[int] = None


class BaseLLM(ABC):
    """Abstract interface for all LLM backends.

    Every backend (Ollama, OpenAI, HuggingFace) must implement this.
    The rest of the framework only interacts with this interface,
    making model swaps a config-level change.
    """

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Return the model identifier string."""
        ...

    @abstractmethod
    def generate(self, messages: list[Message], config: GenerationConfig) -> str:
        """Generate a response given a conversation history.

        Args:
            messages: Ordered list of messages (system prompt + history).
            config: Generation parameters.

        Returns:
            The model's response as a plain string.
        """
        ...
