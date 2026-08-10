"""HTTP client for Face Change API."""

from typing import Any

import httpx

from face_change_cli.core.config import settings
from face_change_cli.core.exceptions import (
    FaceChangeAPIError,
    FaceChangeAuthError,
    FaceChangeTimeoutError,
)


class FaceChangeClient:
    """HTTP client for AceDataCloud Face Change API."""

    def __init__(self, api_token: str | None = None, base_url: str | None = None):
        self.api_token = api_token if api_token is not None else settings.api_token
        self.base_url = base_url or settings.api_base_url
        self.timeout = settings.request_timeout

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with authentication."""
        if not self.api_token:
            raise FaceChangeAuthError(
                "API token not configured. Set ACEDATACLOUD_API_TOKEN or use --token option."
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
        """Make a POST request to the API."""
        url = f"{self.base_url}{endpoint}"
        request_timeout = timeout or self.timeout
        payload = {k: v for k, v in (payload or {}).items() if v is not None}

        with httpx.Client() as http_client:
            try:
                response = http_client.post(
                    url,
                    json=payload,
                    headers=self._get_headers(),
                    timeout=request_timeout,
                )
                if response.status_code == 401:
                    raise FaceChangeAuthError("Invalid API token")
                if response.status_code == 403:
                    raise FaceChangeAuthError("Access denied. Check your API permissions.")
                response.raise_for_status()
                return response.json()  # type: ignore[no-any-return]
            except httpx.TimeoutException as e:
                raise FaceChangeTimeoutError(
                    f"Request to {endpoint} timed out after {request_timeout}s"
                ) from e
            except FaceChangeAuthError:
                raise
            except httpx.HTTPStatusError as e:
                raise FaceChangeAPIError(
                    message=e.response.text,
                    code=f"http_{e.response.status_code}",
                    status_code=e.response.status_code,
                ) from e
            except Exception as e:
                if isinstance(e, FaceChangeAPIError | FaceChangeTimeoutError):
                    raise
                raise FaceChangeAPIError(message=str(e)) from e

    def analyze(self, **kwargs: Any) -> dict[str, Any]:
        """Analyze facial landmarks using /face/analyze."""
        return self.request("/face/analyze", kwargs)

    def beautify(self, **kwargs: Any) -> dict[str, Any]:
        """Beautify a face image using /face/beautify."""
        return self.request("/face/beautify", kwargs)

    def change_age(self, **kwargs: Any) -> dict[str, Any]:
        """Change face age using /face/change-age."""
        return self.request("/face/change-age", kwargs)

    def change_gender(self, **kwargs: Any) -> dict[str, Any]:
        """Change face gender using /face/change-gender."""
        return self.request("/face/change-gender", kwargs)

    def detect_live(self, **kwargs: Any) -> dict[str, Any]:
        """Detect liveness using /face/detect-live."""
        return self.request("/face/detect-live", kwargs)

    def swap(self, **kwargs: Any) -> dict[str, Any]:
        """Swap faces using /face/swap."""
        return self.request("/face/swap", kwargs)

    def cartoon(self, **kwargs: Any) -> dict[str, Any]:
        """Generate a cartoon face using /face/cartoon."""
        return self.request("/face/cartoon", kwargs)


def get_client(token: str | None = None) -> FaceChangeClient:
    """Get a FaceChangeClient instance, optionally overriding the token."""
    if token:
        return FaceChangeClient(api_token=token)
    return FaceChangeClient()
