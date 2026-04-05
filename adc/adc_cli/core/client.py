"""HTTP client for AceDataCloud API."""

from typing import Any

import httpx

from adc_cli.core.config import settings
from adc_cli.core.exceptions import (
    AdcAPIError,
    AdcAuthError,
    AdcTimeoutError,
)

# Dummy callback URL to force async mode for long-running operations.
_ASYNC_CALLBACK_URL = "https://api.acedata.cloud/health"


class AdcClient:
    """HTTP client for AceDataCloud API."""

    def __init__(self, api_token: str | None = None, base_url: str | None = None):
        self.api_token = api_token if api_token is not None else settings.api_token
        self.base_url = base_url or settings.api_base_url
        self.timeout = settings.request_timeout

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with authentication."""
        if not self.api_token:
            raise AdcAuthError(
                "API token not configured. Set ACEDATACLOUD_API_TOKEN or run 'adc auth login'."
            )
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
        """Make a POST request to the AceDataCloud API."""
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
                    raise AdcAuthError("Invalid API token")

                if response.status_code == 403:
                    raise AdcAuthError("Access denied. Check your API permissions.")

                response.raise_for_status()
                return response.json()  # type: ignore[no-any-return]

            except httpx.TimeoutException as e:
                raise AdcTimeoutError(
                    f"Request to {endpoint} timed out after {request_timeout}s"
                ) from e

            except AdcAuthError:
                raise

            except httpx.HTTPStatusError as e:
                raise AdcAPIError(
                    message=e.response.text,
                    code=f"http_{e.response.status_code}",
                    status_code=e.response.status_code,
                ) from e

            except Exception as e:
                if isinstance(e, AdcAPIError | AdcTimeoutError):
                    raise
                raise AdcAPIError(message=str(e)) from e

    # Service-specific convenience methods
    def flux_image(self, **kwargs: Any) -> dict[str, Any]:
        """Generate/edit image using Flux."""
        return self.request("/flux/images", self._with_async_callback(kwargs))

    def midjourney_imagine(self, **kwargs: Any) -> dict[str, Any]:
        """Generate image using Midjourney."""
        return self.request("/midjourney/imagine", self._with_async_callback(kwargs))

    def suno_music(self, **kwargs: Any) -> dict[str, Any]:
        """Generate music using Suno."""
        return self.request("/suno/audios", self._with_async_callback(kwargs))

    def luma_video(self, **kwargs: Any) -> dict[str, Any]:
        """Generate video using Luma."""
        return self.request("/luma/videos", self._with_async_callback(kwargs))

    def sora_video(self, **kwargs: Any) -> dict[str, Any]:
        """Generate video using Sora."""
        return self.request("/sora/videos", self._with_async_callback(kwargs))

    def serp_search(self, **kwargs: Any) -> dict[str, Any]:
        """Search Google using SERP API."""
        return self.request("/serp/google", kwargs)

    def query_task(self, service: str, **kwargs: Any) -> dict[str, Any]:
        """Query task status."""
        return self.request(f"/{service}/tasks", kwargs)


def get_client(token: str | None = None) -> AdcClient:
    """Get an AdcClient instance, optionally overriding the token."""
    if token:
        return AdcClient(api_token=token)
    return AdcClient()
