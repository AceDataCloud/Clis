"""HTTP client for Gemini AI AceDataCloud API."""

from typing import Any

import httpx

from gemini_cli.core.config import settings
from gemini_cli.core.exceptions import (
    GeminiAPIError,
    GeminiAuthError,
    GeminiTimeoutError,
)


class GeminiClient:
    """HTTP client for AceDataCloud Gemini API."""

    def __init__(self, api_token: str | None = None, base_url: str | None = None):
        self.api_token = api_token if api_token is not None else settings.api_token
        self.base_url = base_url or settings.api_base_url
        self.timeout = settings.request_timeout

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with authentication."""
        if not self.api_token:
            raise GeminiAuthError(
                "API token not configured. "
                "Set ACEDATACLOUD_API_TOKEN or use --token option."
            )
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
        """Make a POST request to the AceDataCloud API."""
        url = f"{self.base_url}{endpoint}"
        request_timeout = timeout or self.timeout

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
                    raise GeminiAuthError("Invalid API token")

                if response.status_code == 403:
                    raise GeminiAuthError("Access denied. Check your API permissions.")

                response.raise_for_status()
                return response.json()  # type: ignore[no-any-return]

            except httpx.TimeoutException as e:
                raise GeminiTimeoutError(
                    f"Request to {endpoint} timed out after {request_timeout}s"
                ) from e

            except GeminiAuthError:
                raise

            except httpx.HTTPStatusError as e:
                raise GeminiAPIError(
                    message=e.response.text,
                    code=f"http_{e.response.status_code}",
                    status_code=e.response.status_code,
                ) from e

            except Exception as e:
                if isinstance(e, GeminiAPIError | GeminiTimeoutError):
                    raise
                raise GeminiAPIError(message=str(e)) from e

    def chat_completions(self, **kwargs: Any) -> dict[str, Any]:
        """Send a chat completion request."""
        return self.request("/gemini/chat/completions", kwargs)

    def generate_content(self, model: str, contents: list) -> dict[str, Any]:
        """Generate content using native Gemini API."""
        url = f"{self.base_url}/v1beta/models/{model}:generateContent"
        payload = {"contents": contents}

        with httpx.Client() as http_client:
            try:
                response = http_client.post(
                    url,
                    json=payload,
                    headers=self._get_headers(),
                    timeout=self.timeout,
                )
                if response.status_code == 401:
                    raise GeminiAuthError("Invalid API token")
                if response.status_code == 403:
                    raise GeminiAuthError("Access denied. Check your API permissions.")
                response.raise_for_status()
                return response.json()  # type: ignore[no-any-return]
            except httpx.TimeoutException as e:
                raise GeminiTimeoutError(f"Request timed out after {self.timeout}s") from e
            except GeminiAuthError:
                raise
            except httpx.HTTPStatusError as e:
                raise GeminiAPIError(
                    message=e.response.text,
                    code=f"http_{e.response.status_code}",
                    status_code=e.response.status_code,
                ) from e
            except Exception as e:
                if isinstance(e, GeminiAPIError | GeminiTimeoutError):
                    raise
                raise GeminiAPIError(message=str(e)) from e


def get_client(token: str | None = None) -> GeminiClient:
    """Get a GeminiClient instance, optionally overriding the token."""
    if token:
        return GeminiClient(api_token=token)
    return GeminiClient()
