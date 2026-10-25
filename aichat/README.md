# AiChat CLI

A command-line tool for AI Dialogue via the [AceDataCloud](https://platform.acedata.cloud?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=aichat_cli_readme_platform) platform.

## Get your Ace Data Cloud API key

1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=aichat_cli_readme_api_key). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=aichat_cli_readme_pricing).
3. Copy the **API Key** from the application card, or open **Keys / Manage Keys → Create** to create a separate key for this integration. Give it a recognizable name so you can revoke or rotate it independently.
4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Enable only the restrictions you need, allow the operations you will call, then click **Create** and copy the token from the key list. Task lookup does not grant permission to submit a generation. Confirm the application's balance can cover your first request; any trial allowance is whatever your account currently displays.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy an application API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the key in the client's credential store or the environment variable shown below. Never put it in a prompt, shared workflow, screenshot, or Git commit. If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.

## Features

- **Chat with AI** — Send questions to GPT, DeepSeek, Grok, GLM, and more models
- **Conversation Continuation** — Resume conversations using `--id`
- **Stateful Sessions** — Enable multi-turn context with `--stateful`
- **References** — Inject context documents into prompts with `--ref`
- **Rich Output** — Beautiful terminal formatting with `--json` for scripting
- **Many Models** — GPT-5, GPT-4o, o3, o4-mini, DeepSeek, Grok, GLM, and more

## Installation

```bash
pip install aichat-pro-cli
```

## Quick Start

```bash
# Set your API token
export ACEDATACLOUD_API_TOKEN=your_token_here

# Ask a question
aichat chat "What is the capital of France?"

# Use a specific model
aichat chat "Explain quantum computing" -m gpt-4o

# Continue a conversation
aichat chat "Tell me more" --id 64a67fff-61dc-4801-8339-2c69334c61d6

# Stateful conversation (server remembers context)
aichat chat "My name is Alice" --stateful
aichat chat "What is my name?" --id <returned-id> --stateful

# With reference documents
aichat chat "Summarize this" --ref "https://example.com/doc.txt"

# Get JSON output
aichat chat "Hello" --json | jq '.answer'
```

## Commands

| Command | Description |
|---------|-------------|
| `chat` | Send a question to an AI model (`/aichat/conversations`) |
| `chat2` | Send a conversation request with structured messages and tool results (`/aichat2/conversations`) |
| `models` | List all available models |
| `models2` | List models available to `chat2` |
| `config` | Show current configuration |

## Chat Options

| Option | Description |
|--------|-------------|
| `-m`, `--model` | Model to use (default: `gpt-4o`) |
| `--id` | Conversation ID to continue |
| `--preset` | Preset model name |
| `--stateful` | Enable stateful conversation |
| `--ref` | Reference URL or text (repeatable) |
| `--json` | Output raw JSON |

## Kimi in Chat2

Use `kimi-k3.1-pro` through `chat2`; `kimi-k3` and `kimi-k2.6` remain available.
Run `aichat models2` for the `chat2` model list, which is separate from `chat`.

```bash
aichat chat2 "Review this code and suggest a fix" -m kimi-k3.1-pro --max-turns 1
```

## Chat2 Turn Limit

`aichat chat2 --max-turns` accepts integers from 1 to 500 and limits agent
iterations (model calls), not conversation history. When omitted, the CLI leaves
`max_turns` out of the request and the server defaults to 500. Each model call is
billed by actual usage; a higher limit allows longer tool chains.

Set the limit to 1 for a single answer without tool calls:

```bash
aichat chat2 "Explain quantum computing" --max-turns 1
```

## Configuration

| Environment Variable | Description | Default |
|---------------------|-------------|---------|
| `ACEDATACLOUD_API_TOKEN` | API authentication token | (required) |
| `ACEDATACLOUD_API_BASE_URL` | API base URL | `https://api.acedata.cloud` |
| `AICHAT_REQUEST_TIMEOUT` | Request timeout in seconds | `30` |

You can also use a `.env` file or pass `--token` directly.

## Docker

```bash
docker compose run aichat-cli chat "Hello!"
```

## Development

```bash
# Install with dev dependencies
pip install -e ".[all]"

# Run tests
pytest

# Run linter
ruff check .
ruff format --check .
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Links

- [AceDataCloud Platform](https://platform.acedata.cloud?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=aichat_cli_readme_platform)
- [API Documentation](https://platform.acedata.cloud/documents?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=aichat_cli_readme_documents)
