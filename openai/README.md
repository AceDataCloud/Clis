# OpenAI CLI

A command-line tool for accessing OpenAI models through the [AceDataCloud](https://platform.acedata.cloud) API.

## Features

- **Chat completions** — Interact with GPT-5.x, GPT-4.x, o1, o3, and o4 models
- **Responses API** — Use the OpenAI Responses API with extended model support
- **Embeddings** — Generate text embedding vectors
- **Image generation** — Create images with DALL-E 3, GPT-Image models
- **Image editing** — Edit images using AI

## Installation

```bash
pip install openai-cli
```

## Quick Start

```bash
# Set your API token
export ACEDATACLOUD_API_TOKEN=your_token

# Chat with GPT
openai chat "What is the capital of France?"

# Use a specific model
openai chat "Explain quantum computing" -m gpt-4o

# Generate an image
openai imagine "A serene mountain landscape at sunset"

# Create embeddings
openai embed "The quick brown fox jumps over the lazy dog"

# Use the Responses API
openai respond "Summarize recent AI developments" -m o3
```

## Commands

### `openai chat`

Send a single user message and get a completion.

```bash
openai chat "Hello, how are you?" -m gpt-4o-mini
openai chat "Write a haiku" --temperature 1.5
openai chat "Be concise" -s "You are a helpful assistant"
```

### `openai complete`

Create a completion from a full JSON messages array.

```bash
openai complete '[{"role":"user","content":"Hello"}]'
openai complete '[{"role":"system","content":"Be brief"},{"role":"user","content":"Hi"}]' -m gpt-4o
```

### `openai embed`

Generate embedding vectors for text.

```bash
openai embed "The quick brown fox"
openai embed "Hello world" -m text-embedding-3-large --dimensions 256
```

### `openai imagine`

Generate images from text prompts.

```bash
openai imagine "A cat on a rooftop at night"
openai imagine "Product photo of a watch" -m gpt-image-1 --quality high
openai imagine "Abstract painting" --size 1536x1024
```

### `openai edit-image`

Edit an existing image using a text prompt.

```bash
openai edit-image "Make the background white" -i https://example.com/photo.jpg
openai edit-image "Add sunglasses to the person" -i photo.jpg -m gpt-image-1
```

### `openai respond`

Use the OpenAI Responses API.

```bash
openai respond "What is 2+2?"
openai respond "Explain AI" -m o3
```

### `openai models`

List all available models.

```bash
openai models
```

### `openai config`

Show current configuration.

```bash
openai config
```

## Configuration

| Environment Variable | Description | Default |
|---|---|---|
| `ACEDATACLOUD_API_TOKEN` | Your AceDataCloud API token | (required) |
| `ACEDATACLOUD_API_BASE_URL` | API base URL | `https://api.acedata.cloud` |
| `OPENAI_REQUEST_TIMEOUT` | Request timeout in seconds | `60` |

Get your API token at [https://platform.acedata.cloud](https://platform.acedata.cloud).

## License

MIT License. See [LICENSE](LICENSE) for details.
