class LLMGatewayError(Exception):
    """Base exception for LLM gateway failures."""


class LLMProviderError(LLMGatewayError):
    """Raised when the configured LLM provider fails."""