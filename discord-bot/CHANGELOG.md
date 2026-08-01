# Changelog

## [0.1.0] - 2026-08-01

### Added
- Initial release of Discord Bot CLI
- `health` command to check service status (`GET /health`)
- `whoami` command to view the current proxied account (`GET /api/whoami`)
- `guilds` command to list joined servers (`GET /api/guilds`)
- `channels` command to list channels in a guild (`GET /api/guilds/{guild_id}/channels`)
- `create-channel` command to create a text channel (`POST /api/guilds/{guild_id}/channels`)
- `members` command to list guild members (`GET /api/guilds/{guild_id}/members`)
- `send` command to send a message to a channel (`POST /api/messages`)
- `messages` command to read recent messages from a channel (`GET /api/channels/{channel_id}/messages`)
- `search` command to search messages in a channel (`GET /api/channels/{channel_id}/messages/search`)
- `edit` command to edit a sent message (`PATCH /api/channels/{channel_id}/messages/{message_id}`)
- `delete` command to delete a message (`DELETE /api/channels/{channel_id}/messages/{message_id}`)
- `react` command to add an emoji reaction (`POST /api/channels/{channel_id}/messages/{message_id}/reactions`)
- `pin` command to pin a message (`POST /api/channels/{channel_id}/messages/{message_id}/pin`)
- `open-dm` command to open a DM channel (`POST /api/dms`)
- `send-dm` command to send a direct message (`POST /api/dms/send`)
- `config` command to show current configuration
