from dataclasses import dataclass, field
from pathlib import Path

import yaml

from src.agents.base import BaseAgent
from src.llm.base import BaseLLM, GenerationConfig, Message


@dataclass
class PersonaConfig:
    """Holds the definition of an agent's ideological persona.

    This is loaded from a YAML file in config/personas/.
    Keeping it as a dataclass (rather than a raw dict) gives us
    type safety and makes it easy to extend with new fields later
    (e.g. a list of forbidden argument types for evaluation).
    """
    name: str           # Human-readable label, e.g. "Utilitarian"
    stance: str         # Short identifier used in logs, e.g. "utilitarian"
    system_prompt: str  # The full conditioning prompt sent as the system message


def load_persona(path: str | Path) -> PersonaConfig:
    """Load a persona definition from a YAML file.

    Args:
        path: Path to a persona YAML file (e.g. config/personas/utilitarian.yaml).

    Returns:
        A PersonaConfig instance populated from the file.
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Persona file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return PersonaConfig(
        name=data["name"],
        stance=data["stance"],
        system_prompt=data["system_prompt"],
    )


class PersonaAgent(BaseAgent):
    """A debate agent conditioned by a persona defined in a YAML file.

    This is the primary agent type for research phases 1–6.
    Stance is operationalized purely through the system prompt.

    How it works:
        Every time respond() is called, the agent builds a message list:
            [system_message (persona)] + [conversation history so far]
        and passes it to the LLM backend. The response is then appended
        to the internal history so future calls remain contextually aware.

    This mirrors how chat models maintain context — the full history is
    re-sent on every call. This is intentional: it lets the model stay
    coherent across rounds without any special memory mechanism.

    Args:
        agent_id:   Unique label for this agent in a debate (e.g. "agent_a").
        llm:        Any BaseLLM backend (Ollama, OpenAI, etc.).
        persona:    PersonaConfig loaded from a YAML file.
        gen_config: GenerationConfig (temperature, max_tokens, seed).
    """

    def __init__(
        self,
        agent_id: str,
        llm: BaseLLM,
        persona: PersonaConfig,
        gen_config: GenerationConfig,
    ) -> None:
        self._id = agent_id
        self._llm = llm
        self._persona = persona
        self._gen_config = gen_config

        # Internal conversation history — grows as the debate progresses.
        # Stored as alternating user/assistant messages (opponent spoke → agent replied).
        self._history: list[Message] = []

    @property
    def agent_id(self) -> str:
        return self._id

    @property
    def stance(self) -> str:
        return self._persona.stance

    def respond(self, message: str) -> str:
        # Treat the incoming message as the "user" turn from this agent's perspective.
        # In a debate, the opponent is always "user" and this agent is always "assistant".
        self._history.append(Message(role="user", content=message))

        # Build the full context: persona system prompt + entire conversation so far.
        # The system message is prepended fresh on every call — it is never stored
        # in self._history, so it can't drift or be overwritten.
        messages = [
            Message(role="system", content=self._persona.system_prompt)
        ] + self._history

        # Call the LLM backend
        response = self._llm.generate(messages, self._gen_config)

        # Record own response as an "assistant" turn for future context
        self._history.append(Message(role="assistant", content=response))

        return response

    def reset(self) -> None:
        # Wipe history so the agent can participate in a new debate cleanly.
        # The persona itself is unchanged — only the conversation context is cleared.
        self._history = []
