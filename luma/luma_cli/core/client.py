"""HTTP client for Luma API."""

from typing import Any

import httpx

from luma_cli.core.config import settings
from luma_cli.core.exceptions import (
    LumaAPIError,
    LumaAuthError,
    LumaTimeoutError,
)


class LumaClient:
    """HTTP client for AceDataCloud Luma API."""

    def __init__(self, api_token: str | None = None, base_url: str | None = None):
        self.api_token = api_token if api_token is not None else settings.api_token
        self.base_url = base_url or settings.api_base_url
        self.timeout = settings.request_timeout

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with authentication."""
        if not self.api_token:
            raise LumaAuthError("API token not configured")
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
        """Make a POST request to the Luma API.

        Args:
            endpoint: API endpoint path
            payload: Request body as dictionary
            timeout: Optional timeout override

        Returns:
            API response as dictionary
        """
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
                    raise LumaAuthError("Invalid API token")

                if response.status_code == 403:
                    raise LumaAuthError("Access denied. Check your API permissions.")

                response.raise_for_status()
                return response.json()  # type: ignore[no-any-return]

            except httpx.TimeoutException as e:
                raise LumaTimeoutError(
                    f"Request to {endpoint} timed out after {request_timeout}s"
                ) from e

            except LumaAuthError:
                raise

            except httpx.HTTPStatusError as e:
                raise LumaAPIError(
                    message=e.response.text,
                    code=f"http_{e.response.status_code}",
                    status_code=e.response.status_code,
                ) from e

            except Exception as e:
                if isinstance(e, (LumaAPIError, LumaTimeoutError)):
                    raise
                raise LumaAPIError(message=str(e)) from e

    # Convenience methods
    def generate_video(self, **kwargs: Any) -> dict[str, Any]:
        """Generate video using the main endpoint."""
        return self.request("/luma/videos", kwargs)

    def extend_video(self, **kwargs: Any) -> dict[str, Any]:
        """Extend a video."""
        return self.request("/luma/videos", kwargs)

    def query_task(self, **kwargs: Any) -> dict[str, Any]:
        """Query task status using the tasks endpoint."""
        return self.request("/luma/tasks", kwargs)


def get_client(token: str | None = None) -> LumaClient:
    """Get a LumaClient instance, optionally overriding the token."""
    if token:
        return LumaClient(api_token=token)
    return LumaClient()
