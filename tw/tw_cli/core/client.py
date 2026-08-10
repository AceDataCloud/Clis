"""HTTP client for Twitter API."""

from typing import Any

import httpx

from tw_cli.core.config import settings
from tw_cli.core.exceptions import (
    TwAPIError,
    TwAuthError,
    TwTimeoutError,
)


class TwClient:
    """HTTP client for AceDataCloud Twitter API."""

    def __init__(self, api_token: str | None = None, base_url: str | None = None):
        self.api_token = api_token if api_token is not None else settings.api_token
        self.base_url = base_url or settings.api_base_url
        self.timeout = settings.request_timeout

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with authentication."""
        if not self.api_token:
            raise TwAuthError(
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
                    raise TwAuthError("Invalid API token")
                if response.status_code == 403:
                    raise TwAuthError("Access denied. Check your API permissions.")
                response.raise_for_status()
                return response.json()  # type: ignore[no-any-return]
            except httpx.TimeoutException as e:
                raise TwTimeoutError(
                    f"Request to {endpoint} timed out after {request_timeout}s"
                ) from e
            except TwAuthError:
                raise
            except httpx.HTTPStatusError as e:
                raise TwAPIError(
                    message=e.response.text,
                    code=f"http_{e.response.status_code}",
                    status_code=e.response.status_code,
                ) from e
            except Exception as e:
                if isinstance(e, TwAPIError | TwTimeoutError):
                    raise
                raise TwAPIError(message=str(e)) from e

    def posts(self, **kwargs: Any) -> dict[str, Any]:
        """Get X posts using /x/posts."""
        return self.request("/x/posts", kwargs)

    def users(self, **kwargs: Any) -> dict[str, Any]:
        """Get X user details using /x/users."""
        return self.request("/x/users", kwargs)

    def retweets(self, **kwargs: Any) -> dict[str, Any]:
        """Find retweets using /x/retweets."""
        return self.request("/x/retweets", kwargs)


def get_client(token: str | None = None) -> TwClient:
    """Get a TwClient instance, optionally overriding the token."""
    if token:
        return TwClient(api_token=token)
    return TwClient()
