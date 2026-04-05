"""HTTP client for SERP API."""

from typing import Any

import httpx

from serp_cli.core.config import settings
from serp_cli.core.exceptions import (
    SerpAPIError,
    SerpAuthError,
    SerpTimeoutError,
)


class SerpClient:
    """HTTP client for AceDataCloud Google SERP API."""

    def __init__(self, api_token: str | None = None, base_url: str | None = None):
        self.api_token = api_token if api_token is not None else settings.api_token
        self.base_url = base_url or settings.api_base_url
        self.timeout = settings.request_timeout

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with authentication."""
        if not self.api_token:
            raise SerpAuthError("API token not configured")
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
        """Make a POST request to the SERP API."""
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
                    raise SerpAuthError("Invalid API token")

                if response.status_code == 403:
                    raise SerpAuthError("Access denied. Check your API permissions.")

                response.raise_for_status()
                return response.json()  # type: ignore[no-any-return]

            except httpx.TimeoutException as e:
                raise SerpTimeoutError(
                    f"Request to {endpoint} timed out after {request_timeout}s"
                ) from e

            except SerpAuthError:
                raise

            except httpx.HTTPStatusError as e:
                raise SerpAPIError(
                    message=e.response.text,
                    code=f"http_{e.response.status_code}",
                    status_code=e.response.status_code,
                ) from e

            except Exception as e:
                if isinstance(e, SerpAPIError | SerpTimeoutError):
                    raise
                raise SerpAPIError(message=str(e)) from e

    def search(self, **kwargs: Any) -> dict[str, Any]:
        """Perform a Google search."""
        return self.request("/serp/google", kwargs)


def get_client(token: str | None = None) -> SerpClient:
    """Get a SerpClient instance, optionally overriding the token."""
    if token:
        return SerpClient(api_token=token)
    return SerpClient()
