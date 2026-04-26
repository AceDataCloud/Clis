# OpenAI CLI

A command-line tool for OpenAI-compatible APIs via [AceDataCloud](https://platform.acedata.cloud).

## Installation

```bash
pip install openai-cli
```

## Quick Start

### 1. Get an API Token

Sign up at [https://platform.acedata.cloud](https://platform.acedata.cloud) and get your API token.

### 2. Configure

```bash
export ACEDATACLOUD_API_TOKEN=your_token_here
```

Or save it to a `.env` file:

```bash
cp .env.example .env
# Edit .env and set ACEDATACLOUD_API_TOKEN
```

### 3. Use

```bash
# Chat with a model
openai-cli chat "What is the capital of France?"

# Chat with a specific model
openai-cli chat "Explain quantum computing" -m gpt-5.4

# Generate embeddings
openai-cli embed "Hello, world!" -m text-embedding-3-small

# Generate an image
openai-cli image "A futuristic city skyline at night"

# Edit an image
openai-cli edit "Add a rainbow" --image-url https://example.com/photo.jpg

# Use the Responses API
openai-cli response "Summarize this article" -m gpt-4o

# Retrieve an async task result
openai-cli tasks retrieve --id 7489df4c-ef03-4de0-b598-e9a590793434
openai-cli tasks retrieve --trace-id my-custom-trace-001

# Retrieve a batch of task results
openai-cli tasks batch --trace-ids trace-001 trace-002

# List available models
openai-cli models

# Show configuration
openai-cli config
```

## Commands

| Command | Description |
|---------|-------------|
| `chat` | Chat completions (`/openai/chat/completions`) |
| `embed` | Text embeddings (`/openai/embeddings`) |
| `image` | Image generation (`/openai/images/generations`) |
| `edit` | Image editing (`/openai/images/edits`) |
| `response` | Responses API (`/openai/responses`) |
| `tasks retrieve` | Retrieve a single async task result (`/openai/tasks`) |
| `tasks batch` | Retrieve multiple async task results (`/openai/tasks`) |
| `models` | List available models |
| `config` | Show current configuration |

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ACEDATACLOUD_API_TOKEN` | Your API token (required) | — |
| `ACEDATACLOUD_API_BASE_URL` | API base URL | `https://api.acedata.cloud` |
| `OPENAI_REQUEST_TIMEOUT` | Request timeout in seconds | `30` |

## Docker

```bash
docker compose run --rm openai-cli chat "Hello!" -m gpt-4o
```
