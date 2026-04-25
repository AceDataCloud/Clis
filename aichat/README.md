# AiChat CLI

A command-line tool for AI Dialogue via the [AceDataCloud](https://platform.acedata.cloud) platform.

## Features

- **Chat with AI** — Send questions to GPT, DeepSeek, Grok, GLM, and more models
- **Conversation Continuation** — Resume conversations using `--id`
- **Stateful Sessions** — Enable multi-turn context with `--stateful`
- **References** — Inject context documents into prompts with `--ref`
- **Rich Output** — Beautiful terminal formatting with `--json` for scripting
- **Many Models** — GPT-5, GPT-4o, o3, o4-mini, DeepSeek, Grok, GLM, and more

## Installation

```bash
pip install aichat-cli
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
| `models` | List all available models |
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

- [AceDataCloud Platform](https://platform.acedata.cloud)
- [API Documentation](https://docs.acedata.cloud)
