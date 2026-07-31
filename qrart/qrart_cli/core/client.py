"""HTTP client for QRArt API."""

from typing import Any

import httpx

from qrart_cli.core.config import settings
from qrart_cli.core.exceptions import (
    QRArtAPIError,
    QRArtAuthError,
    QRArtTimeoutError,
)


class QRArtClient:
    """HTTP client for AceDataCloud QRArt (Art QR Code) API."""

    def __init__(self, api_token: str | None = None, base_url: str | None = None):
        self.api_token = api_token if api_token is not None else settings.api_token
        self.base_url = base_url or settings.api_base_url
        self.timeout = settings.request_timeout

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with authentication."""
        if not self.api_token:
            raise QRArtAuthError(
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
        """Make a POST request to the QRArt API."""
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
                    raise QRArtAuthError("Invalid API token")

                if response.status_code == 403:
                    raise QRArtAuthError("Access denied. Check your API permissions.")

                response.raise_for_status()
                return response.json()  # type: ignore[no-any-return]

            except httpx.TimeoutException as e:
                raise QRArtTimeoutError(
                    f"Request to {endpoint} timed out after {request_timeout}s"
                ) from e

            except QRArtAuthError:
                raise

            except httpx.HTTPStatusError as e:
                raise QRArtAPIError(
                    message=e.response.text,
                    code=f"http_{e.response.status_code}",
                    status_code=e.response.status_code,
                ) from e

            except Exception as e:
                if isinstance(e, QRArtAPIError | QRArtTimeoutError):
                    raise
                raise QRArtAPIError(message=str(e)) from e

    def generate(self, **kwargs: Any) -> dict[str, Any]:
        """Generate an art QR code."""
        return self.request("/qrart/generate", kwargs)

    def query_task(self, **kwargs: Any) -> dict[str, Any]:
        """Query task status."""
        return self.request("/qrart/tasks", kwargs)


def get_client(token: str | None = None) -> QRArtClient:
    """Get a QRArtClient instance, optionally overriding the token."""
    if token:
        return QRArtClient(api_token=token)
    return QRArtClient()
