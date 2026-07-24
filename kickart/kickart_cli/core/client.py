"""HTTP client for Kickart API."""

from typing import Any

import httpx

from kickart_cli.core.config import settings
from kickart_cli.core.exceptions import (
    KickartAPIError,
    KickartAuthError,
    KickartTimeoutError,
)


class KickartClient:
    """HTTP client for AceDataCloud Kickart API."""

    def __init__(self, api_token: str | None = None, base_url: str | None = None):
        self.api_token = api_token if api_token is not None else settings.api_token
        self.base_url = base_url or settings.api_base_url
        self.timeout = settings.request_timeout

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with authentication."""
        if not self.api_token:
            raise KickartAuthError(
                "API token not configured. "
                "Set ACEDATACLOUD_API_TOKEN or use --token option."
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
        """Make a POST request to the Kickart API."""
        url = f"{self.base_url}{endpoint}"
        request_timeout = timeout or self.timeout
        payload = payload or {}

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
                    raise KickartAuthError("Invalid API token")

                if response.status_code == 403:
                    raise KickartAuthError("Access denied. Check your API permissions.")

                response.raise_for_status()
                return response.json()  # type: ignore[no-any-return]

            except httpx.TimeoutException as e:
                raise KickartTimeoutError(
                    f"Request to {endpoint} timed out after {request_timeout}s"
                ) from e

            except KickartAuthError:
                raise

            except httpx.HTTPStatusError as e:
                raise KickartAPIError(
                    message=e.response.text,
                    code=f"http_{e.response.status_code}",
                    status_code=e.response.status_code,
                ) from e

            except Exception as e:
                if isinstance(e, KickartAPIError | KickartTimeoutError):
                    raise
                raise KickartAPIError(message=str(e)) from e

    def generate_video(self, **kwargs: Any) -> dict[str, Any]:
        """Generate an e-commerce video using /kickart/videos."""
        return self.request("/kickart/videos", kwargs)

    def generate_viral_video(self, **kwargs: Any) -> dict[str, Any]:
        """Generate a viral video using /kickart/viral-videos."""
        return self.request("/kickart/viral-videos", kwargs)

    def generate_template_video(self, **kwargs: Any) -> dict[str, Any]:
        """Generate a template video using /kickart/template-videos."""
        return self.request("/kickart/template-videos", kwargs)


def get_client(token: str | None = None) -> KickartClient:
    """Get a KickartClient instance, optionally overriding the token."""
    if token:
        return KickartClient(api_token=token)
    return KickartClient()
