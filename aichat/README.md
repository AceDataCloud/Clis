# AiChat CLI

A command-line tool for AI Dialogue via the [AceDataCloud](https://platform.acedata.cloud) platform.

## Features

- **AI Chat** — Converse with powerful LLMs (GPT-5.x, GPT-4.x, DeepSeek, Grok, GLM, and more)
- **Stateful Conversations** — Maintain conversation history across messages with `--stateful`
- **Reference Injection** — Provide external references/context to ground responses
- **Rich Output** — Beautiful terminal formatting with `--json` for scripting
- **Many Models** — Full support for all available models

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

# Continue a conversation (stateful)
aichat chat "Hello!" --stateful
aichat chat "What did I just say?" --stateful --id <conversation-id>

# Provide references
aichat chat "Summarize this" -r "https://example.com/article"

# Get JSON output
aichat chat "Hello world" --json
```

## Commands

| Command | Description |
|---------|-------------|
| `chat` | Send a question and get an AI-generated answer |
| `models` | List available models |
| `config` | Show current configuration |

## Chat Options

| Option | Description |
|--------|-------------|
| `-m`, `--model` | Model to use (default: gpt-4o) |
| `--id` | Conversation ID to continue an existing conversation |
| `--preset` | Preset model configuration |
| `--stateful` | Enable stateful (multi-turn) conversation mode |
| `-r`, `--reference` | Reference URL or text (can be specified multiple times) |
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
