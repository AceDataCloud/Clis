"""HTTP client for Flux API."""

from typing import Any

import httpx

from flux_cli.core.config import settings
from flux_cli.core.exceptions import (
    FluxAPIError,
    FluxAuthError,
    FluxTimeoutError,
)

# Dummy callback URL to force async mode.
_ASYNC_CALLBACK_URL = "https://api.acedata.cloud/health"


class FluxClient:
    """HTTP client for AceDataCloud Flux API."""

    def __init__(self, api_token: str | None = None, base_url: str | None = None):
        self.api_token = api_token if api_token is not None else settings.api_token
        self.base_url = base_url or settings.api_base_url
        self.timeout = settings.request_timeout

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with authentication."""
        if not self.api_token:
            raise FluxAuthError("API token not configured")
        return {
            "accept": "application/json",
            "authorization": f"Bearer {self.api_token}",
            "content-type": "application/json",
        }

    def _with_async_callback(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Ensure long-running operations are submitted asynchronously."""
        request_payload = dict(payload)
        if not request_payload.get("callback_url"):
            request_payload["callback_url"] = _ASYNC_CALLBACK_URL
        return request_payload

    def request(
        self,
        endpoint: str,
        payload: dict[str, Any],
        timeout: float | None = None,
    ) -> dict[str, Any]:
        """Make a POST request to the Flux API."""
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
                    raise FluxAuthError("Invalid API token")

                if response.status_code == 403:
                    raise FluxAuthError("Access denied. Check your API permissions.")

                response.raise_for_status()
                return response.json()  # type: ignore[no-any-return]

            except httpx.TimeoutException as e:
                raise FluxTimeoutError(
                    f"Request to {endpoint} timed out after {request_timeout}s"
                ) from e

            except FluxAuthError:
                raise

            except httpx.HTTPStatusError as e:
                raise FluxAPIError(
                    message=e.response.text,
                    code=f"http_{e.response.status_code}",
                    status_code=e.response.status_code,
                ) from e

            except Exception as e:
                if isinstance(e, FluxAPIError | FluxTimeoutError):
                    raise
                raise FluxAPIError(message=str(e)) from e

    # Convenience methods
    def generate_image(self, **kwargs: Any) -> dict[str, Any]:
        """Generate image using the images endpoint."""
        return self.request("/flux/images", self._with_async_callback(kwargs))

    def edit_image(self, **kwargs: Any) -> dict[str, Any]:
        """Edit image using the images endpoint."""
        return self.request("/flux/images", self._with_async_callback(kwargs))

    def query_task(self, **kwargs: Any) -> dict[str, Any]:
        """Query task status using the tasks endpoint."""
        return self.request("/flux/tasks", kwargs)


def get_client(token: str | None = None) -> FluxClient:
    """Get a FluxClient instance, optionally overriding the token."""
    if token:
        return FluxClient(api_token=token)
    return FluxClient()
