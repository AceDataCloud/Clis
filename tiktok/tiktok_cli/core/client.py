"""HTTP client for TikTok API."""

from typing import Any

import httpx

from tiktok_cli.core.config import settings
from tiktok_cli.core.exceptions import (
    TikTokAPIError,
    TikTokAuthError,
    TikTokTimeoutError,
)


class TikTokClient:
    """HTTP client for AceDataCloud TikTok API."""

    def __init__(self, api_token: str | None = None, base_url: str | None = None):
        self.api_token = api_token if api_token is not None else settings.api_token
        self.base_url = base_url or settings.api_base_url
        self.timeout = settings.request_timeout

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with authentication."""
        if not self.api_token:
            raise TikTokAuthError(
                "API token not configured. Set ACEDATACLOUD_API_TOKEN or use --token option."
            )
        return {
            "accept": "application/json",
            "authorization": "Bearer " + self.api_token,
            "content-type": "application/json",
        }

    def request(
        self,
        endpoint: str,
        payload: dict[str, Any] | None = None,
        timeout: float | None = None,
    ) -> dict[str, Any]:
        """Make a POST request to the API."""
        url = f"{self.base_url}{endpoint}"
        request_timeout = timeout or self.timeout
        payload = {k: v for k, v in (payload or {}).items() if v is not None}

        with httpx.Client() as http_client:
            try:
                response = http_client.post(
                    url,
                    json=payload,
                    headers=self._get_headers(),
                    timeout=request_timeout,
                )
                if response.status_code == 401:
                    raise TikTokAuthError("Invalid API token")
                if response.status_code == 403:
                    raise TikTokAuthError("Access denied. Check your API permissions.")
                response.raise_for_status()
                return response.json()  # type: ignore[no-any-return]
            except httpx.TimeoutException as e:
                raise TikTokTimeoutError(
                    f"Request to {endpoint} timed out after {request_timeout}s"
                ) from e
            except TikTokAuthError:
                raise
            except httpx.HTTPStatusError as e:
                raise TikTokAPIError(
                    message=e.response.text,
                    code=f"http_{e.response.status_code}",
                    status_code=e.response.status_code,
                ) from e
            except Exception as e:
                if isinstance(e, TikTokAPIError | TikTokTimeoutError):
                    raise
                raise TikTokAPIError(message=str(e)) from e

    def posts(self, **kwargs: Any) -> dict[str, Any]:
        """Get TikTok user posts using /tiktok/posts."""
        return self.request("/tiktok/posts", kwargs)

    def search(self, **kwargs: Any) -> dict[str, Any]:
        """Search TikTok resources using /tiktok/search."""
        return self.request("/tiktok/search", kwargs)

    def user(self, **kwargs: Any) -> dict[str, Any]:
        """Get TikTok user details using /tiktok/user."""
        return self.request("/tiktok/user", kwargs)

    def video(self, **kwargs: Any) -> dict[str, Any]:
        """Get TikTok video details using /tiktok/video."""
        return self.request("/tiktok/video", kwargs)


def get_client(token: str | None = None) -> TikTokClient:
    """Get a TikTokClient instance, optionally overriding the token."""
    if token:
        return TikTokClient(api_token=token)
    return TikTokClient()
