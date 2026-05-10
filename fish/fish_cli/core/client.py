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
            raise FishAuthError("API token not configured")
        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {self.api_token}",
            "content-type": "application/json",
        }
        if extra:
            headers.update(extra)
        return headers

    def _handle_response(self, response: httpx.Response) -> dict[str, Any]:
        """Handle an HTTP response, raising appropriate exceptions on error."""
        if response.status_code == 401:
            raise FishAuthError("Invalid API token")

        if response.status_code == 403:
            raise FishAuthError("Access denied. Check your API permissions.")

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise FishAPIError(
                message=e.response.text,
                code=f"http_{e.response.status_code}",
                status_code=e.response.status_code,
            ) from e

        return response.json()  # type: ignore[no-any-return]

    def post(
        self,
        endpoint: str,
        payload: dict[str, Any],
        extra_headers: dict[str, str] | None = None,
        timeout: float | None = None,
    ) -> dict[str, Any]:
        """Make a POST request to the Fish API.

        Args:
            endpoint: API endpoint path
            payload: Request body as dictionary
            extra_headers: Additional headers to merge (e.g. model selection)
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
                    headers=self._get_headers(extra_headers),
                    timeout=request_timeout,
                )
                return self._handle_response(response)

            except httpx.TimeoutException as e:
                raise FishTimeoutError(
                    f"Request to {endpoint} timed out after {request_timeout}s"
                ) from e

            except (FishAuthError, FishAPIError, FishTimeoutError):
                raise

            except Exception as e:
                raise FishAPIError(message=str(e)) from e

    def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        timeout: float | None = None,
    ) -> dict[str, Any]:
        """Make a GET request to the Fish API.

        Args:
            endpoint: API endpoint path
            params: Query parameters (None values are filtered out)
            timeout: Optional timeout override

        Returns:
            API response as dictionary
        """
        url = f"{self.base_url}{endpoint}"
        request_timeout = timeout or self.timeout

        # Remove None values from query params
        clean_params = {k: v for k, v in (params or {}).items() if v is not None}

        with httpx.Client() as http_client:
            try:
                response = http_client.get(
                    url,
                    params=clean_params,
                    headers=self._get_headers(),
                    timeout=request_timeout,
                )
                return self._handle_response(response)

            except httpx.TimeoutException as e:
                raise FishTimeoutError(
                    f"Request to {endpoint} timed out after {request_timeout}s"
                ) from e

            except (FishAuthError, FishAPIError, FishTimeoutError):
                raise

            except Exception as e:
                raise FishAPIError(message=str(e)) from e

    # Convenience methods

    def synthesize(self, model: str | None = None, **kwargs: Any) -> dict[str, Any]:
        """Synthesize text to speech via POST /fish/tts."""
        extra_headers: dict[str, str] = {}
        if model:
            extra_headers["model"] = model
        return self.post("/fish/tts", kwargs, extra_headers=extra_headers or None)

    def list_voices(self, **kwargs: Any) -> dict[str, Any]:
        """List voice models via GET /fish/model."""
        return self.get("/fish/model", params=kwargs)

    def get_voice(self, voice_id: str) -> dict[str, Any]:
        """Get a specific voice model via GET /fish/model/{id}."""
        return self.get(f"/fish/model/{voice_id}")

    def query_task(self, **kwargs: Any) -> dict[str, Any]:
        """Query task status via POST /fish/tasks."""
        return self.post("/fish/tasks", kwargs)


def get_client(token: str | None = None) -> FishClient:
    """Get a FishClient instance, optionally overriding the token."""
    if token:
        return FishClient(api_token=token)
    return FishClient()
