"""HTTP client for Localization API."""

from typing import Any

import httpx

from localization_cli.core.config import settings
from localization_cli.core.exceptions import (
    LocalizationAPIError,
    LocalizationAuthError,
    LocalizationTimeoutError,
)


class LocalizationClient:
    """HTTP client for AceDataCloud Localization API."""

    def __init__(self, api_token: str | None = None, base_url: str | None = None):
        self.api_token = api_token if api_token is not None else settings.api_token
        self.base_url = base_url or settings.api_base_url
        self.timeout = settings.request_timeout

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with authentication."""
        if not self.api_token:
            raise LocalizationAuthError(
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
        """Make a POST request to the Localization API."""
        url = f"{self.base_url}{endpoint}"
        request_timeout = timeout or self.timeout
        payload = payload or {}
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
                    raise LocalizationAuthError("Invalid API token")

                if response.status_code == 403:
                    raise LocalizationAuthError("Access denied. Check your API permissions.")

                response.raise_for_status()
                return response.json()  # type: ignore[no-any-return]

            except httpx.TimeoutException as e:
                raise LocalizationTimeoutError(
                    f"Request to {endpoint} timed out after {request_timeout}s"
                ) from e

            except LocalizationAuthError:
                raise

            except httpx.HTTPStatusError as e:
                raise LocalizationAPIError(
                    message=e.response.text,
                    code=f"http_{e.response.status_code}",
                    status_code=e.response.status_code,
                ) from e

            except Exception as e:
                if isinstance(e, LocalizationAPIError | LocalizationTimeoutError):
                    raise
                raise LocalizationAPIError(message=str(e)) from e

    def translate(self, **kwargs: Any) -> dict[str, Any]:
        """Translate a JSON input into any localized file."""
        return self.request("/localization/translate", kwargs)


def get_client(token: str | None = None) -> LocalizationClient:
    """Get a LocalizationClient instance, optionally overriding the token."""
    if token:
        return LocalizationClient(api_token=token)
    return LocalizationClient()
