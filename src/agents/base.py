from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """Abstract interface for all debate agents.

    An agent is the unit of participation in a debate. It receives a message
    from its opponent, generates a response, and maintains its own conversation
    history internally.

    Every concrete agent type (persona-conditioned, fine-tuned, etc.) must
    implement this interface. The debate controller only interacts with this
    interface — it never knows what kind of agent it is talking to.
    """

    @property
    @abstractmethod
    def agent_id(self) -> str:
        """Unique identifier for this agent within a debate run (e.g. 'agent_a')."""
        ...

    @property
    @abstractmethod
    def stance(self) -> str:
        """Short label describing this agent's ideological stance (e.g. 'utilitarian').

        Used by the logger and evaluation module to tag outputs.
        """
        ...

    @abstractmethod
    def respond(self, message: str) -> str:
        """Generate a response to the given message.

        The agent internally appends the incoming message and its own response
        to its conversation history before returning.

        Args:
            message: The opponent's latest message, as a plain string.

        Returns:
            The agent's response as a plain string.
        """
        ...

    @abstractmethod
    def reset(self) -> None:
        """Clear the agent's conversation history.

        Call this between debate runs so the agent starts fresh.
        Without this, history from a previous debate would bleed into the next.
        """
        ...
