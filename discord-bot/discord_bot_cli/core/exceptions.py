"""Custom exceptions for Discord Bot CLI."""


class DiscordBotError(Exception):
    """Base exception for Discord Bot CLI."""

    def __init__(self, message: str, code: str = "unknown"):
        self.message = message
        self.code = code
        super().__init__(message)


class DiscordBotAuthError(DiscordBotError):
    """Authentication error."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, code="auth_error")


class DiscordBotAPIError(DiscordBotError):
    """API error with HTTP status code."""

    def __init__(
        self,
        message: str = "API request failed",
        code: str = "api_error",
        status_code: int | None = None,
    ):
        self.status_code = status_code
        super().__init__(message, code)


class DiscordBotTimeoutError(DiscordBotError):
    """Request timeout error."""

    def __init__(self, message: str = "Request timed out"):
        super().__init__(message, code="timeout_error")


class DiscordBotConfigError(DiscordBotError):
    """Configuration error."""

    def __init__(self, message: str = "Service not configured"):
        super().__init__(message, code="config_error")
