"""HTTP client for WebExtrator API."""

from typing import Any

import httpx

from webextrator_cli.core.config import settings
from webextrator_cli.core.exceptions import (
    WebExtraterAPIError,
    WebExtraterAuthError,
    WebExtraterTimeoutError,
)


class WebExtraterClient:
    """HTTP client for AceDataCloud WebExtrator API."""

    def __init__(self, api_token: str | None = None, base_url: str | None = None):
        self.api_token = api_token if api_token is not None else settings.api_token
        self.base_url = base_url or settings.api_base_url
        self.timeout = settings.request_timeout

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with authentication."""
        if not self.api_token:
            raise WebExtraterAuthError(
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
        """Make a POST request to the WebExtrator API."""
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
                    raise WebExtraterAuthError("Invalid API token")

                if response.status_code == 403:
                    raise WebExtraterAuthError("Access denied. Check your API permissions.")

                response.raise_for_status()
                return response.json()  # type: ignore[no-any-return]

            except httpx.TimeoutException as e:
                raise WebExtraterTimeoutError(
                    f"Request to {endpoint} timed out after {request_timeout}s"
                ) from e

            except WebExtraterAuthError:
                raise

            except httpx.HTTPStatusError as e:
                raise WebExtraterAPIError(
                    message=e.response.text,
                    code=f"http_{e.response.status_code}",
                    status_code=e.response.status_code,
                ) from e

            except Exception as e:
                if isinstance(e, WebExtraterAPIError | WebExtraterTimeoutError):
                    raise
                raise WebExtraterAPIError(message=str(e)) from e

    def extract(self, **kwargs: Any) -> dict[str, Any]:
        """Extract structured content from a web page."""
        return self.request("/webextrator/extract", kwargs)

    def render(self, **kwargs: Any) -> dict[str, Any]:
        """Render a web page and return the HTML."""
        return self.request("/webextrator/render", kwargs)

    def tasks(self, **kwargs: Any) -> dict[str, Any]:
        """Query previously created render/extract tasks."""
        return self.request("/webextrator/tasks", kwargs)


def get_client(token: str | None = None) -> WebExtraterClient:
    """Get a WebExtraterClient instance, optionally overriding the token."""
    if token:
        return WebExtraterClient(api_token=token)
    return WebExtraterClient()
