"""HTTP client for Midjourney API."""

from typing import Any

import httpx

from midjourney_cli.core.config import settings
from midjourney_cli.core.exceptions import (
    MidjourneyAPIError,
    MidjourneyAuthError,
    MidjourneyTimeoutError,
)


class MidjourneyClient:
    """HTTP client for AceDataCloud Midjourney API."""

    def __init__(self, api_token: str | None = None, base_url: str | None = None):
        self.api_token = api_token if api_token is not None else settings.api_token
        self.base_url = base_url or settings.api_base_url
        self.timeout = settings.request_timeout

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with authentication."""
        if not self.api_token:
            raise MidjourneyAuthError("API token not configured")
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
        """Make a POST request to the Midjourney API.

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
                    raise MidjourneyAuthError("Invalid API token")

                if response.status_code == 403:
                    raise MidjourneyAuthError("Access denied. Check your API permissions.")

                response.raise_for_status()
                return response.json()  # type: ignore[no-any-return]

            except httpx.TimeoutException as e:
                raise MidjourneyTimeoutError(
                    f"Request to {endpoint} timed out after {request_timeout}s"
                ) from e

            except MidjourneyAuthError:
                raise

            except httpx.HTTPStatusError as e:
                raise MidjourneyAPIError(
                    message=e.response.text,
                    code=f"http_{e.response.status_code}",
                    status_code=e.response.status_code,
                ) from e

            except Exception as e:
                if isinstance(e, MidjourneyAPIError | MidjourneyTimeoutError):
                    raise
                raise MidjourneyAPIError(message=str(e)) from e

    # Convenience methods
    def imagine(self, **kwargs: Any) -> dict[str, Any]:
        """Generate image using the imagine endpoint."""
        return self.request("/midjourney/imagine", kwargs)

    def seed(self, **kwargs: Any) -> dict[str, Any]:
        """Retrieve seed for an image."""
        return self.request("/midjourney/seed", kwargs)

    def edits(self, **kwargs: Any) -> dict[str, Any]:
        """Edit an image using the edits endpoint."""
        return self.request("/midjourney/edits", kwargs)

    def videos(self, **kwargs: Any) -> dict[str, Any]:
        """Generate a video using the videos endpoint."""
        return self.request("/midjourney/videos", kwargs)

    def describe(self, **kwargs: Any) -> dict[str, Any]:
        """Describe an image using the describe endpoint."""
        return self.request("/midjourney/describe", kwargs)

    def shorten(self, **kwargs: Any) -> dict[str, Any]:
        """Shorten a prompt using the shorten endpoint."""
        return self.request("/midjourney/shorten", kwargs)

    def translate(self, **kwargs: Any) -> dict[str, Any]:
        """Translate content using the translate endpoint."""
        return self.request("/midjourney/translate", kwargs)

    def query_task(self, **kwargs: Any) -> dict[str, Any]:
        """Query task status using the tasks endpoint."""
        return self.request("/midjourney/tasks", kwargs)


def get_client(token: str | None = None) -> MidjourneyClient:
    """Get a MidjourneyClient instance, optionally overriding the token."""
    if token:
        return MidjourneyClient(api_token=token)
    return MidjourneyClient()
