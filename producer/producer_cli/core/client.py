"""HTTP client for Producer API."""

from typing import Any

import httpx

from producer_cli.core.config import settings
from producer_cli.core.exceptions import (
    ProducerAPIError,
    ProducerAuthError,
    ProducerTimeoutError,
)


class ProducerClient:
    """HTTP client for AceDataCloud Producer API."""

    def __init__(self, api_token: str | None = None, base_url: str | None = None):
        self.api_token = api_token if api_token is not None else settings.api_token
        self.base_url = base_url or settings.api_base_url
        self.timeout = settings.request_timeout

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with authentication."""
        if not self.api_token:
            raise ProducerAuthError("API token not configured")
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
        """Make a POST request to the Producer API.

        Args:
            endpoint: API endpoint path
            payload: Request body as dictionary
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
                    headers=self._get_headers(),
                    timeout=request_timeout,
                )

                if response.status_code == 401:
                    raise ProducerAuthError("Invalid API token")

                if response.status_code == 403:
                    raise ProducerAuthError("Access denied. Check your API permissions.")

                response.raise_for_status()
                return response.json()  # type: ignore[no-any-return]

            except httpx.TimeoutException as e:
                raise ProducerTimeoutError(
                    f"Request to {endpoint} timed out after {request_timeout}s"
                ) from e

            except ProducerAuthError:
                raise

            except httpx.HTTPStatusError as e:
                raise ProducerAPIError(
                    message=e.response.text,
                    code=f"http_{e.response.status_code}",
                    status_code=e.response.status_code,
                ) from e

            except Exception as e:
                if isinstance(e, ProducerAPIError | ProducerTimeoutError):
                    raise
                raise ProducerAPIError(message=str(e)) from e

    # Convenience methods
    def generate_audio(self, **kwargs: Any) -> dict[str, Any]:
        """Generate audio using the audios endpoint."""
        return self.request("/producer/audios", kwargs)

    def generate_lyrics(self, **kwargs: Any) -> dict[str, Any]:
        """Generate lyrics using the lyrics endpoint."""
        return self.request("/producer/lyrics", kwargs)

    def upload_audio(self, **kwargs: Any) -> dict[str, Any]:
        """Upload audio from a URL."""
        return self.request("/producer/upload", kwargs)

    def generate_video(self, **kwargs: Any) -> dict[str, Any]:
        """Generate a video from an audio."""
        return self.request("/producer/videos", kwargs)

    def get_wav(self, **kwargs: Any) -> dict[str, Any]:
        """Get WAV format of an audio."""
        return self.request("/producer/wav", kwargs)

    def query_task(self, **kwargs: Any) -> dict[str, Any]:
        """Query task status using the tasks endpoint."""
        return self.request("/producer/tasks", kwargs)


def get_client(token: str | None = None) -> ProducerClient:
    """Get a ProducerClient instance, optionally overriding the token."""
    if token:
        return ProducerClient(api_token=token)
    return ProducerClient()
