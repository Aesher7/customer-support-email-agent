"""LLM service for interacting with OpenAI."""

from langchain_openai import ChatOpenAI
from src.core.config import get_settings
from src.services.base import BaseService


class LLMService(BaseService):
    """Service for LLM operations."""

    def __init__(self, db=None):
        """Initialize LLM service."""
        super().__init__(db)
        self.settings = get_settings()
        self.llm = self._init_llm()

    def _init_llm(self) -> ChatOpenAI:
        """Initialize LLM instance."""
        return ChatOpenAI(
            model="gpt-4",
            api_key=self.settings.openai_api_key,
            temperature=0.7,
        )

    def invoke(self, messages: list) -> str:
        """
        Invoke LLM with messages.

        Args:
            messages: List of messages

        Returns:
            LLM response
        """
        try:
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            self.logger.error(f"Error invoking LLM: {e}")
            raise


# Global LLM service instance
_llm_service = None


def get_llm_service(db=None) -> LLMService:
    """Get or create LLM service instance."""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService(db)
    return _llm_service
