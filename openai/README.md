# OpenAI CLI

A command-line tool for OpenAI-compatible APIs via [AceDataCloud](https://platform.acedata.cloud?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=openai_cli_readme_platform).

## Installation

```bash
pip install openai-pro-cli
```

## Quick Start

### 1. Get API Token

1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=openai_cli_readme_api_key). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=openai_cli_readme_pricing).
3. Copy the **API Key** from the application card, or open **Keys / Manage Keys → Create** to create a separate key for this integration. Give it a recognizable name so you can revoke or rotate it independently.
4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Enable only the restrictions you need, allow the operations you will call, then click **Create** and copy the token from the key list. Task lookup does not grant permission to submit a generation. Confirm the application's balance can cover your first request; any trial allowance is whatever your account currently displays.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy an application API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the key in the client's credential store or the environment variable shown below. Never put it in a prompt, shared workflow, screenshot, or Git commit. If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.

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
