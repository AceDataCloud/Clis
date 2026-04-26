# Kimi CLI

A command-line tool for Kimi chat completions via [AceDataCloud](https://platform.acedata.cloud).

## Installation

```bash
pip install kimi-cli
```

## Quick Start

### 1. Get an API Token

Sign up at [https://platform.acedata.cloud](https://platform.acedata.cloud) and get your API token.

### 2. Configure

```bash
export ACEDATACLOUD_API_TOKEN=your_token_here
```

### 3. Use

```bash
# Chat with a model
kimi-cli chat "What is the capital of France?"

# Chat with a specific model
kimi-cli chat "Explain quantum computing" -m kimi-k2-thinking

# List available models
kimi-cli models

# Show configuration
kimi-cli config
```

## Commands

| Command | Description |
|---------|-------------|
| `chat`  | Chat completions (`/kimi/chat/completions`) |
| `models` | List available models |
| `config` | Show current configuration |

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ACEDATACLOUD_API_TOKEN` | Your API token (required) | — |
| `ACEDATACLOUD_API_BASE_URL` | API base URL | `https://api.acedata.cloud` |
| `KIMI_REQUEST_TIMEOUT` | Request timeout in seconds | `30` |

## Docker

```bash
docker compose run --rm kimi-cli chat "Hello!"
```
