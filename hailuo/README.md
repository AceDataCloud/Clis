# Hailuo CLI

A command-line tool for generating AI videos using [Hailuo (MiniMax)](https://platform.acedata.cloud?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=hailuo_cli_readme_platform) through the AceDataCloud platform.

## Get your Ace Data Cloud API key

1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=hailuo_cli_readme_api_key). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=hailuo_cli_readme_pricing).
3. Copy the **API Key** from the application card, or open **Keys / Manage Keys → Create** to create a separate key for this integration. Give it a recognizable name so you can revoke or rotate it independently.
4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Enable only the restrictions you need, allow the operations you will call, then click **Create** and copy the token from the key list. Task lookup does not grant permission to submit a generation. Confirm the application's balance can cover your first request; any trial allowance is whatever your account currently displays.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy an application API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the key in the client's credential store or the environment variable shown below. Never put it in a prompt, shared workflow, screenshot, or Git commit. If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.

## Installation

```bash
pip install hailuo-cli
```

## Configuration

```bash
export ACEDATACLOUD_API_TOKEN=your_token
```

Or copy `.env.example` to `.env` and fill in your token.

## Commands

### Video Generation

| Command | Description |
|---------|-------------|
| `hailuo generate <prompt>` | Generate a video from text (MiniMax-H3) |
| `hailuo image-to-video <prompt> --image-url <url>` | Generate video from image + text |

### Task Management

| Command | Description |
|---------|-------------|
| `hailuo task <task_id>` | Query a single task status |
| `hailuo tasks <id1> <id2> [...]` | Query multiple tasks at once |
| `hailuo delete <task_id>` | Delete a task |
| `hailuo wait <task_id>` | Wait for task completion with polling |

### Utilities

| Command | Description |
|---------|-------------|
| `hailuo models` | List available Hailuo models |
| `hailuo config` | Show current configuration |

## Global Options

```
--token TEXT    API token (or set ACEDATACLOUD_API_TOKEN env var)
--version       Show version
--help          Show help message
```

Most commands support:

```
--json          Output raw JSON (for piping/scripting)
--callback-url  Webhook URL for async notifications
```

## Examples

```bash
# Generate a video from a text prompt
hailuo generate "A cat playing in the snow"

# Generate from image reference
hailuo image-to-video "Animate the scene" --image-url https://example.com/photo.jpg

# Use a specific model
hailuo generate "Ocean waves" --model MiniMax-H3

# Check task status
hailuo task abc123-def456

# Wait for completion
hailuo wait abc123 --timeout 300
```

## Docker

```bash
# Pull the image
docker pull ghcr.io/acedatacloud/hailuo-cli:latest

# Run a command
docker run --rm -e ACEDATACLOUD_API_TOKEN=your_token \
  ghcr.io/acedatacloud/hailuo-cli generate "A happy scene"

# Or use docker-compose
docker compose run --rm hailuo-cli generate "A happy scene"
```

## Project Structure

```
HailuoCli/
├── hailuo_cli/             # Main package
│   ├── __init__.py
│   ├── __main__.py         # python -m hailuo_cli entry point
│   ├── main.py             # CLI entry point
│   ├── core/               # Core modules
│   │   ├── client.py       # HTTP client for Hailuo API
│   │   ├── config.py       # Configuration management
│   │   ├── exceptions.py   # Custom exceptions
│   │   └── output.py       # Rich terminal formatting
│   └── commands/           # CLI command groups
│       ├── video.py        # Video generation commands
│       ├── task.py         # Task management commands
│       └── info.py         # Info and utility commands
└── tests/                  # Test suite
```

## License

MIT License — see [LICENSE](LICENSE) for details.
