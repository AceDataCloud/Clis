# Discord Bot CLI

A command-line tool for interacting with a self-hosted [Discord Agent Proxy](https://platform.acedata.cloud/console/applications) service from AceDataCloud.

## Overview

Discord Agent Proxy is a self-deployed service that maintains a persistent connection to Discord on behalf of your account, and exposes it via REST API and MCP. This CLI wraps the REST API.

> ⚠️ **Warning:** Automating a personal Discord account (self-bot) violates Discord's Terms of Service. Use a dedicated secondary account and operate responsibly.

## Installation

```bash
pip install discord-bot-cli
```

## Setup

1. Deploy your Discord Agent Proxy instance at [platform.acedata.cloud](https://platform.acedata.cloud/console/applications)
2. Configure your Discord account credentials in the console
3. Note your service URL and access token

```bash
export DISCORD_BOT_BASE_URL=https://discord-bot-xxxxxxxxxxxx.app.acedata.cloud
export DISCORD_BOT_TOKEN=your_access_token
```

Or copy `.env.example` to `.env` and fill in the values.

## Usage

```bash
# Check service health
discord-bot health

# View current account
discord-bot whoami

# List guilds (servers)
discord-bot guilds

# List channels in a guild
discord-bot channels 1234567890

# Create a channel
discord-bot create-channel 1234567890 general

# List members
discord-bot members 1234567890

# Send a message
discord-bot send 1234567890 "Hello!"

# Reply to a message
discord-bot send 1234567890 "Got it" --reply-to 9876543210

# Send with idempotency key (safe retries)
discord-bot send 1234567890 "Hello!" --idempotency-key msg-20260816-001

# Read recent messages
discord-bot messages 1234567890 --limit 20

# Search messages
discord-bot search 1234567890 "release date"

# Edit a message
discord-bot edit 1234567890 9876543210 "Updated content"

# Delete a message
discord-bot delete 1234567890 9876543210

# Add a reaction
discord-bot react 1234567890 9876543210 "👍"

# Pin a message
discord-bot pin 1234567890 9876543210

# Open a DM channel
discord-bot open-dm 111222333444555666

# Send a DM
discord-bot send-dm 111222333444555666 "Hello!"
```

Use `--json` on any command for raw JSON output.

## Commands

| Command | Description |
|---|---|
| `health` | Check service health and gateway status |
| `whoami` | View current proxied account |
| `guilds` | List joined servers |
| `channels GUILD_ID` | List channels in a server |
| `create-channel GUILD_ID NAME` | Create a text channel |
| `members GUILD_ID` | List server members |
| `send CHANNEL_ID CONTENT` | Send a message |
| `messages CHANNEL_ID` | Read recent messages |
| `search CHANNEL_ID QUERY` | Search messages |
| `edit CHANNEL_ID MESSAGE_ID CONTENT` | Edit a message |
| `delete CHANNEL_ID MESSAGE_ID` | Delete a message |
| `react CHANNEL_ID MESSAGE_ID EMOJI` | Add a reaction |
| `pin CHANNEL_ID MESSAGE_ID` | Pin a message |
| `open-dm RECIPIENT_ID` | Open a DM channel |
| `send-dm RECIPIENT_ID CONTENT` | Send a direct message |
| `config` | Show current configuration |

## License

MIT
