"""HTTP client for AiChat API."""

from typing import Any

import httpx

from aichat_cli.core.config import settings
from aichat_cli.core.exceptions import (
    AichatAPIError,
    AichatAuthError,
    AichatTimeoutError,
)


class AichatClient:
    """HTTP client for AceDataCloud AI Dialogue API."""

    def __init__(self, api_token: str | None = None, base_url: str | None = None):
        self.api_token = api_token if api_token is not None else settings.api_token
        self.base_url = base_url or settings.api_base_url
        self.timeout = settings.request_timeout

    def _get_headers(self, accept: str = "application/json") -> dict[str, str]:
        """Get request headers with authentication."""
        if not self.api_token:
            raise AichatAuthError("API token not configured")
        return {
            "accept": accept,
            "authorization": f"Bearer {self.api_token}",
            "content-type": "application/json",
        }

    def request(
        self,
        endpoint: str,
        payload: dict[str, Any],
        timeout: float | None = None,
    ) -> dict[str, Any]:
        """Make a POST request to the AiChat API."""
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
                    raise AichatAuthError("Invalid API token")

                if response.status_code == 403:
                    raise AichatAuthError("Access denied. Check your API permissions.")

                response.raise_for_status()
                return response.json()  # type: ignore[no-any-return]

            except httpx.TimeoutException as e:
                raise AichatTimeoutError(
                    f"Request to {endpoint} timed out after {request_timeout}s"
                ) from e

            except AichatAuthError:
                raise

            except httpx.HTTPStatusError as e:
                raise AichatAPIError(
                    message=e.response.text,
                    code=f"http_{e.response.status_code}",
                    status_code=e.response.status_code,
                ) from e

            except Exception as e:
                if isinstance(e, AichatAPIError | AichatTimeoutError):
                    raise
                raise AichatAPIError(message=str(e)) from e

    def converse(self, **kwargs: Any) -> dict[str, Any]:
        """Send a conversation request to the AI."""
        return self.request("/aichat/conversations", kwargs)


def get_client(token: str | None = None) -> AichatClient:
    """Get an AichatClient instance, optionally overriding the token."""
    if token:
        return AichatClient(api_token=token)
    return AichatClient()
