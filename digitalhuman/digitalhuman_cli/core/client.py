"""HTTP client for Digital Human API."""

from typing import Any

import httpx

from digitalhuman_cli.core.config import settings
from digitalhuman_cli.core.exceptions import (
    DigitalHumanAPIError,
    DigitalHumanAuthError,
    DigitalHumanTimeoutError,
)


class DigitalHumanClient:
    """HTTP client for AceDataCloud Digital Human API."""

    def __init__(self, api_token: str | None = None, base_url: str | None = None):
        self.api_token = api_token if api_token is not None else settings.api_token
        self.base_url = base_url or settings.api_base_url
        self.timeout = settings.request_timeout

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with authentication."""
        if not self.api_token:
            raise DigitalHumanAuthError(
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
        """Make a POST request to the Digital Human API."""
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
                    raise DigitalHumanAuthError("Invalid API token")

                if response.status_code == 403:
                    raise DigitalHumanAuthError("Access denied. Check your API permissions.")

                response.raise_for_status()
                return response.json()  # type: ignore[no-any-return]

            except httpx.TimeoutException as e:
                raise DigitalHumanTimeoutError(
                    f"Request to {endpoint} timed out after {request_timeout}s"
                ) from e

            except DigitalHumanAuthError:
                raise

            except httpx.HTTPStatusError as e:
                raise DigitalHumanAPIError(
                    message=e.response.text,
                    code=f"http_{e.response.status_code}",
                    status_code=e.response.status_code,
                ) from e

            except Exception as e:
                if isinstance(e, DigitalHumanAPIError | DigitalHumanTimeoutError):
                    raise
                raise DigitalHumanAPIError(message=str(e)) from e

    def generate_video(self, **kwargs: Any) -> dict[str, Any]:
        """Generate a digital human video."""
        return self.request("/digital-human/videos", kwargs)

    def clone_voice(self, **kwargs: Any) -> dict[str, Any]:
        """Clone a voice from audio."""
        return self.request("/digital-human/voices", kwargs)

    def query_task(self, **kwargs: Any) -> dict[str, Any]:
        """Query task status."""
        return self.request("/digital-human/tasks", kwargs)


def get_client(token: str | None = None) -> DigitalHumanClient:
    """Get a DigitalHumanClient instance, optionally overriding the token."""
    if token:
        return DigitalHumanClient(api_token=token)
    return DigitalHumanClient()
