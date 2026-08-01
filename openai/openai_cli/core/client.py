"""HTTP client for OpenAI-compatible AceDataCloud API."""

from typing import Any

import httpx

from openai_cli.core.config import settings
from openai_cli.core.exceptions import (
    OpenAIAPIError,
    OpenAIAuthError,
    OpenAITimeoutError,
)


class OpenAIClient:
    """HTTP client for AceDataCloud OpenAI-compatible API."""

    def __init__(self, api_token: str | None = None, base_url: str | None = None):
        self.api_token = api_token if api_token is not None else settings.api_token
        self.base_url = base_url or settings.api_base_url
        self.timeout = settings.request_timeout

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with authentication."""
        if not self.api_token:
            raise OpenAIAuthError(
                "API token not configured. Set ACEDATACLOUD_API_TOKEN or use --token option."
            )
        return {
            "accept": "application/json",
            "authorization": f"Bearer {self.api_token}",
            "content-type": "application/json",
        }

    def request(
        self,
        endpoint: str,
        payload: dict[str, Any] | None = None,
        timeout: float | None = None,
        method: str = "POST",
    ) -> dict[str, Any]:
        """Make a request to the AceDataCloud API."""
        url = f"{self.base_url}{endpoint}"
        request_timeout = timeout or self.timeout

        payload = payload or {}

        # Remove None values from payload
        payload = {k: v for k, v in payload.items() if v is not None}

        with httpx.Client() as http_client:
            try:
                response = http_client.request(
                    method,
                    url,
                    json=payload if method.upper() != "GET" else None,
                    headers=self._get_headers(),
                    timeout=request_timeout,
                )

                if response.status_code == 401:
                    raise OpenAIAuthError("Invalid API token")

                if response.status_code == 403:
                    raise OpenAIAuthError("Access denied. Check your API permissions.")

                response.raise_for_status()
                return response.json()  # type: ignore[no-any-return]

            except httpx.TimeoutException as e:
                raise OpenAITimeoutError(
                    f"Request to {endpoint} timed out after {request_timeout}s"
                ) from e

            except OpenAIAuthError:
                raise

            except httpx.HTTPStatusError as e:
                raise OpenAIAPIError(
                    message=e.response.text,
                    code=f"http_{e.response.status_code}",
                    status_code=e.response.status_code,
                ) from e

            except Exception as e:
                if isinstance(e, OpenAIAPIError | OpenAITimeoutError):
                    raise
                raise OpenAIAPIError(message=str(e)) from e

    def request_bytes(
        self,
        endpoint: str,
        payload: dict[str, Any] | None = None,
        timeout: float | None = None,
        method: str = "POST",
    ) -> bytes:
        """Make a request that returns binary content."""
        url = f"{self.base_url}{endpoint}"
        request_timeout = timeout or self.timeout

        payload = payload or {}
        payload = {k: v for k, v in payload.items() if v is not None}
        headers = self._get_headers()
        headers["accept"] = "*/*"

        with httpx.Client() as http_client:
            try:
                response = http_client.request(
                    method,
                    url,
                    json=payload if method.upper() != "GET" else None,
                    headers=headers,
                    timeout=request_timeout,
                )

                if response.status_code == 401:
                    raise OpenAIAuthError("Invalid API token")

                if response.status_code == 403:
                    raise OpenAIAuthError("Access denied. Check your API permissions.")

                response.raise_for_status()
                return response.content

            except httpx.TimeoutException as e:
                raise OpenAITimeoutError(
                    f"Request to {endpoint} timed out after {request_timeout}s"
                ) from e

            except OpenAIAuthError:
                raise

            except httpx.HTTPStatusError as e:
                raise OpenAIAPIError(
                    message=e.response.text,
                    code=f"http_{e.response.status_code}",
                    status_code=e.response.status_code,
                ) from e

            except Exception as e:
                if isinstance(e, OpenAIAPIError | OpenAITimeoutError):
                    raise
                raise OpenAIAPIError(message=str(e)) from e

    def chat_completions(self, **kwargs: Any) -> dict[str, Any]:
        """Send a chat completion request."""
        return self.request("/openai/chat/completions", kwargs)

    def embeddings(self, **kwargs: Any) -> dict[str, Any]:
        """Generate embeddings."""
        return self.request("/openai/embeddings", kwargs)

    def image_generations(self, **kwargs: Any) -> dict[str, Any]:
        """Generate images."""
        return self.request("/openai/images/generations", kwargs)

    def image_edits(self, **kwargs: Any) -> dict[str, Any]:
        """Edit images."""
        return self.request("/openai/images/edits", kwargs)

    def responses(self, **kwargs: Any) -> dict[str, Any]:
        """Send a Responses API request."""
        return self.request("/openai/responses", kwargs)

    def request_multipart(
        self,
        endpoint: str,
        fields: dict[str, Any] | None = None,
        files: dict[str, Any] | None = None,
        timeout: float | None = None,
    ) -> dict[str, Any] | str:
        """Make a multipart/form-data request."""
        url = f"{self.base_url}{endpoint}"
        request_timeout = timeout or self.timeout

        if not self.api_token:
            raise OpenAIAuthError(
                "API token not configured. Set ACEDATACLOUD_API_TOKEN or use --token option."
            )
        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {self.api_token}",
        }

        # Build multipart parts as a list so repeated keys (e.g. timestamp_granularities[])
        # are supported.  Plain fields use (None, value); file fields keep their tuple form.
        multipart: list[tuple[str, Any]] = []
        for key, value in (fields or {}).items():
            if value is None:
                continue
            if isinstance(value, list):
                for item in value:
                    multipart.append((key, (None, str(item))))
            else:
                multipart.append((key, (None, str(value))))
        for key, value in (files or {}).items():
            multipart.append((key, value))

        with httpx.Client() as http_client:
            try:
                response = http_client.post(
                    url,
                    files=multipart,
                    headers=headers,
                    timeout=request_timeout,
                )

                if response.status_code == 401:
                    raise OpenAIAuthError("Invalid API token")

                if response.status_code == 403:
                    raise OpenAIAuthError("Access denied. Check your API permissions.")

                response.raise_for_status()
                content_type = response.headers.get("content-type", "")
                if "application/json" in content_type:
                    return response.json()  # type: ignore[no-any-return]
                return response.text

            except httpx.TimeoutException as e:
                raise OpenAITimeoutError(
                    f"Request to {endpoint} timed out after {request_timeout}s"
                ) from e

            except OpenAIAuthError:
                raise

            except httpx.HTTPStatusError as e:
                raise OpenAIAPIError(
                    message=e.response.text,
                    code=f"http_{e.response.status_code}",
                    status_code=e.response.status_code,
                ) from e

            except Exception as e:
                if isinstance(e, OpenAIAPIError | OpenAITimeoutError):
                    raise
                raise OpenAIAPIError(message=str(e)) from e

    def audio_speech(self, **kwargs: Any) -> bytes:
        """Synthesize speech audio."""
        return self.request_bytes("/v1/audio/speech", kwargs)

    def audio_transcriptions(
        self,
        file: bytes,
        filename: str = "audio.wav",
        **kwargs: Any,
    ) -> dict[str, Any] | str:
        """Transcribe audio to text."""
        repeated_fields = {
            "timestamp_granularities": "timestamp_granularities[]",
            "languages": "languages[]",
            "keywords": "keywords[]",
        }
        fields = dict(kwargs)
        for source_name, target_name in repeated_fields.items():
            values = kwargs.pop(source_name, None)
            if values:
                fields[target_name] = values
                fields.pop(source_name, None)
        return self.request_multipart(
            "/v1/audio/transcriptions",
            fields=fields,
            files={"file": (filename, file, "application/octet-stream")},
        )

    def tasks(self, **kwargs: Any) -> dict[str, Any]:
        """Query OpenAI async task results."""
        return self.request("/openai/tasks", kwargs)

    def models(self) -> dict[str, Any]:
        """List available models from API."""
        return self.request("/openai/models", payload=None, method="GET")


def get_client(token: str | None = None) -> OpenAIClient:
    """Get an OpenAIClient instance, optionally overriding the token."""
    if token:
        return OpenAIClient(api_token=token)
    return OpenAIClient()
