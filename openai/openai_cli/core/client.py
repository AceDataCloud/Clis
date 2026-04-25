"""HTTP client for OpenAI API."""

from typing import Any

import httpx

from openai_cli.core.config import settings
from openai_cli.core.exceptions import (
    OpenAIAPIError,
    OpenAIAuthError,
    OpenAITimeoutError,
)


class OpenAIClient:
    """HTTP client for AceDataCloud OpenAI API."""

    def __init__(self, api_token: str | None = None, base_url: str | None = None):
        self.api_token = api_token if api_token is not None else settings.api_token
        self.base_url = base_url or settings.api_base_url
        self.timeout = settings.request_timeout

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with authentication."""
        if not self.api_token:
            raise OpenAIAuthError("API token not configured")
        return {
            "accept": "application/json",
            "authorization": f"Bearer {self.api_token}",
            "content-type": "application/json",
        }

    def request(
        self,
        endpoint: str,
        payload: dict[str, Any],
        timeout: float | None = None,
    ) -> dict[str, Any]:
        """Make a POST request to the OpenAI API."""
        url = f"{self.base_url}{endpoint}"
        request_timeout = timeout or self.timeout

        # Remove None values from payload
        payload = {k: v for k, v in payload.items() if v is not None}

        with httpx.Client() as http_client:
            try:
                response = http_client.post(
                    url,
                    json=payload,
                    headers=self._get_headers(),
                    timeout=request_timeout,
                )

                if response.status_code == 401:
                    raise OpenAIAuthError("Invalid API token")

                if response.status_code == 403:
                    raise OpenAIAuthError("Access denied. Check your API permissions.")

                response.raise_for_status()
                return response.json()  # type: ignore[no-any-return]

            except httpx.TimeoutException as e:
                raise OpenAITimeoutError(
                    f"Request to {endpoint} timed out after {request_timeout}s"
                ) from e

            except OpenAIAuthError:
                raise

            except httpx.HTTPStatusError as e:
                raise OpenAIAPIError(
                    message=e.response.text,
                    code=f"http_{e.response.status_code}",
                    status_code=e.response.status_code,
                ) from e

            except Exception as e:
                if isinstance(e, OpenAIAPIError | OpenAITimeoutError):
                    raise
                raise OpenAIAPIError(message=str(e)) from e

    def chat(self, **kwargs: Any) -> dict[str, Any]:
        """Create a chat completion."""
        return self.request("/openai/chat/completions", kwargs)

    def embed(self, **kwargs: Any) -> dict[str, Any]:
        """Create an embedding vector."""
        return self.request("/openai/embeddings", kwargs)

    def generate_image(self, **kwargs: Any) -> dict[str, Any]:
        """Generate an image."""
        return self.request("/openai/images/generations", kwargs)

    def edit_image(self, **kwargs: Any) -> dict[str, Any]:
        """Edit an image."""
        return self.request("/openai/images/edits", kwargs)

    def respond(self, **kwargs: Any) -> dict[str, Any]:
        """Create a response using the Responses API."""
        return self.request("/openai/responses", kwargs)


def get_client(token: str | None = None) -> OpenAIClient:
    """Get an OpenAIClient instance, optionally overriding the token."""
    if token:
        return OpenAIClient(api_token=token)
    return OpenAIClient()
