"""HTTP client for Discord Bot REST API."""

from typing import Any

import httpx

from discord_bot_cli.core.config import settings
from discord_bot_cli.core.exceptions import (
    DiscordBotAPIError,
    DiscordBotAuthError,
    DiscordBotConfigError,
    DiscordBotTimeoutError,
)


class DiscordBotClient:
    """HTTP client for the self-hosted Discord Agent Proxy REST API."""

    def __init__(
        self,
        base_url: str | None = None,
        token: str | None = None,
    ):
        self.base_url = (base_url or settings.base_url).rstrip("/")
        self.token = token if token is not None else settings.token
        self.timeout = settings.request_timeout

        if not self.base_url:
            raise DiscordBotConfigError(
                "Discord Bot base URL not configured. "
                "Set DISCORD_BOT_BASE_URL or use --base-url option."
            )

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with authentication."""
        if not self.token:
            raise DiscordBotAuthError(
                "Access token not configured. Set DISCORD_BOT_TOKEN or use --token option."
            )
        return {
            "accept": "application/json",
            "authorization": self.token,
            "content-type": "application/json",
        }

    def _handle_response(self, response: httpx.Response) -> dict[str, Any]:
        """Handle HTTP response, raising appropriate exceptions."""
        if response.status_code == 401:
            raise DiscordBotAuthError(
                "Invalid token. Ensure the Authorization header matches the console token."
            )
        if response.status_code == 403:
            raise DiscordBotAuthError("Access denied. Check your token permissions.")
        if response.status_code == 503:
            raise DiscordBotAPIError(
                "Service unavailable. The Discord gateway connection is not ready. "
                "Check /health for gateway_ready status.",
                status_code=503,
            )
        response.raise_for_status()
        return response.json()  # type: ignore[no-any-return]

    def _request(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Make an HTTP request to the Discord Bot API."""
        url = f"{self.base_url}{path}"

        # Remove None values from params and json body
        if params:
            params = {k: v for k, v in params.items() if v is not None}
        if json:
            json = {k: v for k, v in json.items() if v is not None}

        with httpx.Client() as http_client:
            try:
                response = http_client.request(
                    method,
                    url,
                    params=params or None,
                    json=json or None,
                    headers=self._get_headers() | (headers or {}),
                    timeout=self.timeout,
                )
                return self._handle_response(response)

            except httpx.TimeoutException as e:
                raise DiscordBotTimeoutError(
                    f"Request to {path} timed out after {self.timeout}s"
                ) from e

            except (DiscordBotAuthError, DiscordBotAPIError, DiscordBotTimeoutError):
                raise

            except httpx.HTTPStatusError as e:
                raise DiscordBotAPIError(
                    message=e.response.text,
                    code=f"http_{e.response.status_code}",
                    status_code=e.response.status_code,
                ) from e

            except Exception as e:
                raise DiscordBotAPIError(message=str(e)) from e

    # Health
    def health(self) -> dict[str, Any]:
        """Check service health (no auth required)."""
        url = f"{self.base_url}/health"
        with httpx.Client() as http_client:
            try:
                response = http_client.get(url, timeout=self.timeout)
                response.raise_for_status()
                return response.json()  # type: ignore[no-any-return]
            except httpx.TimeoutException as e:
                raise DiscordBotTimeoutError(f"Health check timed out after {self.timeout}s") from e
            except httpx.HTTPStatusError as e:
                raise DiscordBotAPIError(
                    message=e.response.text,
                    code=f"http_{e.response.status_code}",
                    status_code=e.response.status_code,
                ) from e

    # Account
    def whoami(self) -> dict[str, Any]:
        """Get the current proxied account info."""
        return self._request("GET", "/api/whoami")

    # Guilds
    def list_guilds(self) -> dict[str, Any]:
        """List guilds the account has joined."""
        return self._request("GET", "/api/guilds")

    def list_channels(self, guild_id: str) -> dict[str, Any]:
        """List channels in a guild."""
        return self._request("GET", f"/api/guilds/{guild_id}/channels")

    def create_channel(self, guild_id: str, name: str) -> dict[str, Any]:
        """Create a text channel in a guild."""
        return self._request("POST", f"/api/guilds/{guild_id}/channels", json={"name": name})

    def list_members(self, guild_id: str, limit: int | None = None) -> dict[str, Any]:
        """List members of a guild."""
        return self._request("GET", f"/api/guilds/{guild_id}/members", params={"limit": limit})

    # Messages
    def send_message(
        self,
        channel_id: str,
        content: str,
        reply_to: str | None = None,
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        """Send a message to a channel."""
        return self._request(
            "POST",
            "/api/messages",
            json={"channel_id": channel_id, "content": content, "reply_to": reply_to},
            headers={"idempotency-key": idempotency_key} if idempotency_key else None,
        )

    def read_messages(self, channel_id: str, limit: int | None = None) -> dict[str, Any]:
        """Read recent messages from a channel."""
        return self._request(
            "GET",
            f"/api/channels/{channel_id}/messages",
            params={"limit": limit},
        )

    def search_messages(
        self, channel_id: str, query: str, limit: int | None = None
    ) -> dict[str, Any]:
        """Search messages in a channel."""
        return self._request(
            "GET",
            f"/api/channels/{channel_id}/messages/search",
            params={"q": query, "limit": limit},
        )

    def edit_message(
        self, channel_id: str, message_id: str, content: str
    ) -> dict[str, Any]:
        """Edit a message."""
        return self._request(
            "PATCH",
            f"/api/channels/{channel_id}/messages/{message_id}",
            json={"content": content},
        )

    def delete_message(self, channel_id: str, message_id: str) -> dict[str, Any]:
        """Delete a message."""
        return self._request(
            "DELETE",
            f"/api/channels/{channel_id}/messages/{message_id}",
        )

    def add_reaction(
        self, channel_id: str, message_id: str, emoji: str
    ) -> dict[str, Any]:
        """Add a reaction to a message."""
        return self._request(
            "POST",
            f"/api/channels/{channel_id}/messages/{message_id}/reactions",
            json={"emoji": emoji},
        )

    def pin_message(self, channel_id: str, message_id: str) -> dict[str, Any]:
        """Pin a message."""
        return self._request(
            "POST",
            f"/api/channels/{channel_id}/messages/{message_id}/pin",
        )

    # DMs
    def open_dm(self, recipient_id: str) -> dict[str, Any]:
        """Open a DM channel with a user."""
        return self._request("POST", "/api/dms", json={"recipient_id": recipient_id})

    def send_dm(self, recipient_id: str, content: str) -> dict[str, Any]:
        """Send a direct message to a user."""
        return self._request(
            "POST",
            "/api/dms/send",
            json={"recipient_id": recipient_id, "content": content},
        )


def get_client(base_url: str | None = None, token: str | None = None) -> DiscordBotClient:
    """Get a DiscordBotClient instance."""
    return DiscordBotClient(base_url=base_url, token=token)
