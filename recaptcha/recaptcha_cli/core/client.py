"""HTTP client for recaptcha API."""

from typing import Any

import httpx

from recaptcha_cli.core.config import settings
from recaptcha_cli.core.exceptions import (
    RecaptchaAPIError,
    RecaptchaAuthError,
    RecaptchaTimeoutError,
)


class RecaptchaClient:
    """HTTP client for AceDataCloud recaptcha API."""

    def __init__(self, api_token: str | None = None, base_url: str | None = None):
        self.api_token = api_token if api_token is not None else settings.api_token
        self.base_url = base_url or settings.api_base_url
        self.timeout = settings.request_timeout

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with authentication."""
        if not self.api_token:
            raise RecaptchaAuthError(
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
        """Make a POST request to the recaptcha API.

        Args:
            endpoint: API endpoint path
            payload: Request body as dictionary
            timeout: Optional timeout override

        Returns:
            API response as dictionary
        """
        url = f"{self.base_url}{endpoint}"
        request_timeout = timeout or self.timeout
        payload = payload or {}

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
                    raise RecaptchaAuthError("Invalid API token")

                if response.status_code == 403:
                    raise RecaptchaAuthError("Access denied. Check your API permissions.")

                response.raise_for_status()
                return response.json()  # type: ignore[no-any-return]

            except httpx.TimeoutException as e:
                raise RecaptchaTimeoutError(
                    f"Request to {endpoint} timed out after {request_timeout}s"
                ) from e

            except RecaptchaAuthError:
                raise

            except httpx.HTTPStatusError as e:
                raise RecaptchaAPIError(
                    message=e.response.text,
                    code=f"http_{e.response.status_code}",
                    status_code=e.response.status_code,
                ) from e

            except Exception as e:
                if isinstance(e, RecaptchaAPIError | RecaptchaTimeoutError):
                    raise
                raise RecaptchaAPIError(message=str(e)) from e

    def recognize(self, **kwargs: Any) -> dict[str, Any]:
        """Recognize recaptcha2 using the /captcha/recognition/recaptcha2 endpoint."""
        return self.request("/captcha/recognition/recaptcha2", kwargs)

    def get_token2(self, **kwargs: Any) -> dict[str, Any]:
        """Get reCAPTCHA v2 token using the /captcha/token/recaptcha2 endpoint."""
        return self.request("/captcha/token/recaptcha2", kwargs)

    def get_token3(self, **kwargs: Any) -> dict[str, Any]:
        """Get reCAPTCHA v3 token using the /captcha/token/recaptcha3 endpoint."""
        return self.request("/captcha/token/recaptcha3", kwargs)


def get_client(token: str | None = None) -> RecaptchaClient:
    """Get a RecaptchaClient instance, optionally overriding the token."""
    if token:
        return RecaptchaClient(api_token=token)
    return RecaptchaClient()
