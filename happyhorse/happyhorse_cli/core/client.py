"""HTTP client for HappyHorse API."""

from typing import Any

import httpx

from happyhorse_cli.core.config import settings
from happyhorse_cli.core.exceptions import (
    HappyHorseAPIError,
    HappyHorseAuthError,
    HappyHorseTimeoutError,
)


class HappyHorseClient:
    """HTTP client for AceDataCloud HappyHorse API."""

    def __init__(self, api_token: str | None = None, base_url: str | None = None):
        self.api_token = api_token if api_token is not None else settings.api_token
        self.base_url = base_url or settings.api_base_url
        self.timeout = settings.request_timeout

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with authentication."""
        if not self.api_token:
            raise HappyHorseAuthError("API token not configured")
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
        """Make a POST request to the HappyHorse API.

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
                    raise HappyHorseAuthError("Invalid API token")

                if response.status_code == 403:
                    raise HappyHorseAuthError("Access denied. Check your API permissions.")

                response.raise_for_status()
                return response.json()  # type: ignore[no-any-return]

            except httpx.TimeoutException as e:
                raise HappyHorseTimeoutError(
                    f"Request to {endpoint} timed out after {request_timeout}s"
                ) from e

            except HappyHorseAuthError:
                raise

            except httpx.HTTPStatusError as e:
                raise HappyHorseAPIError(
                    message=e.response.text,
                    code=f"http_{e.response.status_code}",
                    status_code=e.response.status_code,
                ) from e

            except Exception as e:
                if isinstance(e, HappyHorseAPIError | HappyHorseTimeoutError):
                    raise
                raise HappyHorseAPIError(message=str(e)) from e

    # Convenience methods
    def generate_video(self, **kwargs: Any) -> dict[str, Any]:
        """Generate video using the videos endpoint."""
        return self.request("/happyhorse/videos", kwargs)

    def query_task(self, **kwargs: Any) -> dict[str, Any]:
        """Query task status using the tasks endpoint."""
        return self.request("/happyhorse/tasks", kwargs)


def get_client(token: str | None = None) -> HappyHorseClient:
    """Get a HappyHorseClient instance, optionally overriding the token."""
    if token:
        return HappyHorseClient(api_token=token)
    return HappyHorseClient()
