# Grok CLI

A command-line tool for Grok chat completions via [AceDataCloud](https://platform.acedata.cloud).

## Installation

```bash
pip install grok-cli
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
grok-cli chat "What is the capital of France?"

# Chat with a specific model
grok-cli chat "Explain quantum computing" -m grok-4

# List available models
grok-cli models

# Show configuration
grok-cli config
```

## Commands

| Command | Description |
|---------|-------------|
| `chat`  | Chat completions (`/grok/chat/completions`) |
| `models` | List available models |
| `config` | Show current configuration |

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ACEDATACLOUD_API_TOKEN` | Your API token (required) | — |
| `ACEDATACLOUD_API_BASE_URL` | API base URL | `https://api.acedata.cloud` |
| `GROK_REQUEST_TIMEOUT` | Request timeout in seconds | `30` |

## Docker

```bash
docker compose run --rm grok-cli chat "Hello!"
```
