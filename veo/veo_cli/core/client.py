"""HTTP client for Veo API."""

from typing import Any

import httpx

from veo_cli.core.config import settings
from veo_cli.core.exceptions import (
    VeoAPIError,
    VeoAuthError,
    VeoTimeoutError,
)


class VeoClient:
    """HTTP client for AceDataCloud Veo API."""

    def __init__(self, api_token: str | None = None, base_url: str | None = None):
        self.api_token = api_token if api_token is not None else settings.api_token
        self.base_url = base_url or settings.api_base_url
        self.timeout = settings.request_timeout

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with authentication."""
        if not self.api_token:
            raise VeoAuthError("API token not configured")
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
        """Make a POST request to the Veo API.

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
                    raise VeoAuthError("Invalid API token")

                if response.status_code == 403:
                    raise VeoAuthError("Access denied. Check your API permissions.")

                response.raise_for_status()
                return response.json()  # type: ignore[no-any-return]

            except httpx.TimeoutException as e:
                raise VeoTimeoutError(
                    f"Request to {endpoint} timed out after {request_timeout}s"
                ) from e

            except VeoAuthError:
                raise

            except httpx.HTTPStatusError as e:
                raise VeoAPIError(
                    message=e.response.text,
                    code=f"http_{e.response.status_code}",
                    status_code=e.response.status_code,
                ) from e

            except Exception as e:
                if isinstance(e, VeoAPIError | VeoTimeoutError):
                    raise
                raise VeoAPIError(message=str(e)) from e

    # Convenience methods
    def generate_video(self, **kwargs: Any) -> dict[str, Any]:
        """Generate video using the main endpoint."""
        return self.request("/veo/videos", kwargs)

    def upscale_video(self, **kwargs: Any) -> dict[str, Any]:
        """Upscale a video to 1080p (legacy alias for /veo/videos action=get1080p)."""
        return self.request("/veo/videos", kwargs)

    def upsample_video(self, **kwargs: Any) -> dict[str, Any]:
        """Upsample a video using the dedicated /veo/upsample endpoint.

        Accepts action: 1080p / 4k / gif. Successor to upscale_video; the
        legacy upscale_video method is preserved for backward compatibility.
        """
        return self.request("/veo/upsample", kwargs)

    def extend_video(self, **kwargs: Any) -> dict[str, Any]:
        """Extend the duration of a previously generated video (veo31 series only)."""
        return self.request("/veo/extend", kwargs)

    def reshoot_video(self, **kwargs: Any) -> dict[str, Any]:
        """Re-render a video with a different camera motion."""
        return self.request("/veo/reshoot", kwargs)

    def manipulate_object(self, **kwargs: Any) -> dict[str, Any]:
        """Insert or remove an object in a previously generated video."""
        return self.request("/veo/objects", kwargs)

    def query_task(self, **kwargs: Any) -> dict[str, Any]:
        """Query task status using the tasks endpoint."""
        return self.request("/veo/tasks", kwargs)


def get_client(token: str | None = None) -> VeoClient:
    """Get a VeoClient instance, optionally overriding the token."""
    if token:
        return VeoClient(api_token=token)
    return VeoClient()
