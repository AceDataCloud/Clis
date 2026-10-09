# OpenAI CLI

A command-line tool for OpenAI-compatible APIs via [AceDataCloud](https://platform.acedata.cloud).

## Installation

```bash
pip install openai-pro-cli
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

# Synthesize speech audio
openai-cli speech "Hello from AceDataCloud" --voice nova --output hello.mp3

# Show realtime WebSocket connection details
openai-cli realtime --model gpt-realtime

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
| `speech` | Speech synthesis (`/v1/audio/speech`) |
| `transcribe` | Audio transcription (`/v1/audio/transcriptions`) |
| `realtime` | Realtime WebSocket connection info (`/v1/realtime`) |
| `tasks retrieve` | Retrieve a single async task result (`/openai/tasks`) |
| `tasks batch` | Retrieve multiple async task results (`/openai/tasks`) |
| `models` | List available models (`/openai/models`) |
| `config` | Show current configuration |

## Embedding models

`embed` supports `text-embedding-3-small` (the default) and `text-embedding-3-large`. The legacy `text-embedding-ada-002` model is retired. When migrating an existing index, regenerate its vectors and rebuild the index; do not mix vectors from the old and new models.

## Nano Banana 2.1 images

Use the public `nano-banana-2.1` model ID for generation or editing. There is no `nano-banana-2.1:official` variant; specify the model explicitly to use it instead of the existing default.

```bash
openai-cli image "A blue ceramic vase on a cream background" -m nano-banana-2.1 -n 2
openai-cli edit "Make the vase green" --image-url https://example.com/photo.jpg -m nano-banana-2.1
openai-cli edit "Make the vase green" --image-file photo.png -m nano-banana-2.1
```

Use `--image-url` for JSON requests or `--image-file` for multipart uploads, not both. For dedicated `1K`/`2K`/`4K` resolution controls, use `nano-banana-pro generate` or `nano-banana-pro edit` from the NanoBanana CLI; the OpenAI-compatible commands use their own request fields.

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
