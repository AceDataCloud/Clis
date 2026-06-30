"""HTTP client for Fish API."""

from typing import Any

import httpx

from fish_cli.core.config import settings
from fish_cli.core.exceptions import (
    FishAPIError,
    FishAuthError,
    FishTimeoutError,
)


class FishClient:
    """HTTP client for AceDataCloud Fish API."""

    def __init__(self, api_token: str | None = None, base_url: str | None = None):
        self.api_token = api_token if api_token is not None else settings.api_token
        self.base_url = base_url or settings.api_base_url
        self.timeout = settings.request_timeout

    def _get_headers(self, extra: dict[str, str] | None = None) -> dict[str, str]:
        """Get request headers with authentication."""
        if not self.api_token:
            raise FishAuthError(
                "API token not configured. "
                "Set ACEDATACLOUD_API_TOKEN or use --token option."
            )
        headers = {
            "accept": "application/json",
            "authorization": "Bearer " + self.api_token,
            "content-type": "application/json",
        }
        if extra:
            headers.update(extra)
        return headers

    def request(
        self,
        endpoint: str,
        payload: dict[str, Any] | None = None,
        method: str = "POST",
        timeout: float | None = None,
        path_params: dict[str, str] | None = None,
        extra_headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Make an HTTP request to the Fish API.

        Args:
            endpoint: API endpoint path (e.g., "/fish/tts")
            payload: Request parameters or body as dictionary
            method: HTTP method to use
            timeout: Optional timeout override
            path_params: Path parameters to substitute in the endpoint URL
            extra_headers: Additional headers to include in the request

        Returns:
            API response as dictionary
        """
        if path_params:
            for key, value in path_params.items():
                endpoint = endpoint.replace(f"{{{key}}}", value)

        url = f"{self.base_url}{endpoint}"
        request_timeout = timeout or self.timeout
        payload = payload or {}
        method = method.upper()

        # Remove None values from payload
        payload = {k: v for k, v in payload.items() if v is not None}

        with httpx.Client() as http_client:
            try:
                if method == "GET":
                    response = http_client.get(
                        url,
                        params=payload,
                        headers=self._get_headers(extra_headers),
                        timeout=request_timeout,
                    )
                else:
                    response = http_client.post(
                        url,
                        json=payload,
                        headers=self._get_headers(extra_headers),
                        timeout=request_timeout,
                    )

                if response.status_code == 401:
                    raise FishAuthError("Invalid API token")

                if response.status_code == 403:
                    raise FishAuthError("Access denied. Check your API permissions.")

                response.raise_for_status()
                return response.json()  # type: ignore[no-any-return]

            except httpx.TimeoutException as e:
                raise FishTimeoutError(
                    f"Request to {endpoint} timed out after {request_timeout}s"
                ) from e

            except FishAuthError:
                raise

            except httpx.HTTPStatusError as e:
                raise FishAPIError(
                    message=e.response.text,
                    code=f"http_{e.response.status_code}",
                    status_code=e.response.status_code,
                ) from e

            except Exception as e:
                if isinstance(e, FishAPIError | FishTimeoutError):
                    raise
                raise FishAPIError(message=str(e)) from e

    def generate_tts(self, model: str | None = None, **kwargs: Any) -> dict[str, Any]:
        """Generate TTS audio using the /fish/tts endpoint."""
        extra_headers = {}
        if model:
            extra_headers["model"] = model
        return self.request("/fish/tts", kwargs, extra_headers=extra_headers)

    def list_models(self, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """List available fish voice models."""
        return self.request("/fish/model", params or {}, method="GET")

    def get_model(self, model_id: str) -> dict[str, Any]:
        """Get a specific fish voice model by ID."""
        return self.request(
            "/fish/model/{id}",
            method="GET",
            path_params={"id": model_id},
        )

    def query_task(self, **kwargs: Any) -> dict[str, Any]:
        """Query task status using the /fish/tasks endpoint."""
        return self.request("/fish/tasks", kwargs)


def get_client(token: str | None = None) -> FishClient:
    """Get a FishClient instance, optionally overriding the token."""
    if token:
        return FishClient(api_token=token)
    return FishClient()
