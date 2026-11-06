# GPT Image and OpenAI APIs by Ace Data Cloud — CLI

## Install the Ace integration

This integration is maintained by **Ace Data Cloud** and uses your Ace API key. It is not an official client published by the model owner. Check the [PyPI package](https://pypi.org/project/openai-pro-cli/) and its AceDataCloud repository before installing.

```bash
python -m pip install openai-pro-cli
openai-cli --help
openai-cli image --help
```

The commands above show local help/reference information and do not submit a generation. Then follow **Get API Token** below: register/sign in, initialize General application if needed, create/copy an application key, and store it in the terminal's `ACEDATACLOUD_API_TOKEN` environment variable. Do not use a platform management token.

Generation follows your account's current service access, balance and pricing. Save the returned task ID and query that **same ID**; do not repeat generation while a task is pending.

OpenAI image generation/editing catalog entries and their companion guides are hidden in mainland China (`cn`). This is regional catalog visibility, not global retirement of the image APIs. Local CLI help/model references do not establish regional availability; check your account's current catalog and permissions before submitting an image request.

```text
openai-cli tasks retrieve --id <task-id>
```

A successful command or running preview does not prove a completed media result. Check the task's terminal outcome and returned media link. [中文首次使用指南](https://github.com/AceDataCloud/Clis/blob/main/docs/SERVICE_PACKAGES_zh-CN.md) · [Service-name package directory](https://github.com/AceDataCloud/Clis/blob/main/docs/SERVICE_PACKAGES.md)


## GPT Image-only MCP service entry

The [GPT Image service guide](https://github.com/AceDataCloud/OpenAIMCP/blob/main/GPT_IMAGE.md) and official Registry entry `io.github.AceDataCloud/mcp-gpt-image` use the existing `mcp-openai-pro` package with `--profile gpt-image`. Install version `2026.10.18.2` or newer and preserve those arguments to expose five image/task tools. This is a dedicated service profile, not a new PyPI package and not the generic hosted OpenAI MCP URL.

```bash
uvx --from 'mcp-openai-pro>=2026.10.18.2' mcp-openai-pro --profile gpt-image
```

Configure the raw application key in this server's environment. The free `gpt_image_list_models` is local reference information; generation still requires an explicit model, current permissions/balance/price and same-task retrieval.


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

## Recent chat model options

`gpt-6.1-terra` is available in `chat` and `response`. Its reasoning levels are
`low`, `medium`, `high`, `xhigh` and `max`, not `minimal` or `none`. Start with
`chat --reasoning-effort low` or `response --reasoning '{"effort":"low"}'`.
Input above 272,000 tokens uses long-context pricing; check current account
access, prices and returned usage before switching models.

`chat` also accepts `mimo-v2.6-pro` and `mimo-v2.6-flash` through the compatible
Chat Completions endpoint, with MiMo service permission. This release covers text
Chat Completions, not MiMo Responses, Messages, multimedia, built-in search or
Batch. Function tools use `--tool-choice auto`; executing tools remains the
application's responsibility. The CLI does not automatically execute tools or
assemble multi-turn tool continuations.

```bash
openai-cli chat "Explain rainbows" --model mimo-v2.6-flash --max-completion-tokens 256 --json
openai-cli chat "Compare these options" --model gpt-6.1-terra --reasoning-effort low --json
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

## Chat and Responses billing

Accepted compatible-model requests are billed for the selected model's input, output and cache usage, not a fixed fee per request. Switching between Chat Completions and Responses does not change this to per-request billing. Check current model prices in the console and the returned `usage.cost` for the charge; billing support alone does not establish model availability or account access.

For Chat Completions, `usage.prompt_tokens` includes cached tokens. Responses input totals also include reported cached tokens. Reported cache usage is settled at the corresponding cache price, so do not add cached tokens to these input totals again.

Use `--json` to inspect the full returned usage, including cache details and `usage.cost` when present; the default terminal summary is not a billing breakdown. These commands submit billable requests:

```bash
openai-cli chat "Hello" -m gpt-4o-mini --json | jq '.usage'
openai-cli response "Hello" -m gpt-4o-mini --json | jq '.usage'
```

## Embedding models

`embed` supports `text-embedding-3-small` (the default) and `text-embedding-3-large`. The legacy `text-embedding-ada-002` model is retired. When migrating an existing index, regenerate its vectors and rebuild the index; do not mix vectors from the old and new models.

## GPT Image quality

`image` and `edit` accept `--quality auto`, `low`, `medium` or `high` for GPT Image models. GPT Image 2.5 and 2.6 Flare/Sunburst, including their `:reverse` and `:official` variants, additionally support `xhigh` and `max`. Editing supports these values with either JSON image URLs or multipart image files. Use `--output-format png`, `jpeg` or `webp` for static images; GPT Image 2.6 variants also support native `gif` animation (see **GPT Image 2.6 GIF and 4K** below). SVG output is not supported.

For GPT Image 2.6, use `gpt-image-2.6-flare` or `gpt-image-2.6-sunburst`, optionally with `:reverse` or `:official`. Pass the full model ID unchanged to `image` or `edit`; `gpt-image-2.6` is not a supported shorthand. For both 2.5 and 2.6 Flare/Sunburst, `:reverse` is an explicit alias of the corresponding unsuffixed model.

GPT Image 2/2.5 unsuffixed models and their `:reverse` aliases have a base rate of 0.19 Credits per successful image; GPT Image 2.6 unsuffixed models and their `:reverse` aliases have a base rate of 0.22 Credits per successful image. Returned token statistics do not change this per-image billing. Account discounts and final charges follow current pricing and usage records. GPT Image 2/2.5 availability recovery may use GPT Image 2.5 Flare without changing the requested model or per-image billing.

`:official` requests are billed on actual token usage, not a fixed per-image charge; 2.6 uses the same token rates as 2.5. Generation meters text input and image output; editing also meters reference-image input. Size and quality affect token usage, and pre-request prices are estimates. These models support `-n 1`–`10`; official usage is aggregated across the response, not multiplied by `n` again. Use URL responses for multiple images because `--response-format b64_json` supports only one.

These commands submit billable requests:

```bash
openai-cli image "A blue ceramic vase on a cream background" -m gpt-image-2.6-flare:reverse --quality xhigh --output-format png
openai-cli edit "Make the vase green" --image-url https://example.com/photo.jpg -m gpt-image-2.6-sunburst:reverse --quality max --output-format webp
openai-cli edit "Make the vase green" --image-file photo.png -m gpt-image-2.6-flare:official --quality max --output-format jpeg
```

Legacy DALL-E quality options are unchanged: `dall-e-3` generation accepts `hd` or `standard`, and `dall-e-2` accepts `standard`.

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


### GPT Image 2.6 GIF and 4K

Use `--output-format gif` with `gpt-image-2.6-flare`, its `:reverse`/`:official` variants, or any `gpt-image-2.6-sunburst` variant. Generation and both URL/file editing accept `--frame-count` and `--frame-duration-ms`. GIF defaults to a 512x512 preview, 9 frames and 200 ms per frame; actual dimensions may be adjusted by the model.

```bash
openai-cli image "A red ball moving left and right, seamless loop" \
  --model gpt-image-2.6-flare --output-format gif --size 512x512 \
  --frame-count 9 --frame-duration-ms 200 --async
```

All 2.6 variants retain static PNG/JPEG/WebP 4K generation and editing with `--size 3840x2160` or `--size 2160x3840`. Use concrete pixels, not `--size 4K`; `4096x4096` exceeds the static pixel budget. GIF has separate size/frame constraints and does not inherit the static 4K presets. `--count` counts returned GIF files, not frames.

GPT Image 2.6 supports `--complexity low`, `medium` or `high` (omitted: model default high). Planning complexity is independent of rendering `--quality` and has no separate surcharge; `:official` still bills actual token usage. Omit `--input-fidelity` for GPT Image 2.6.

Static edits accept `--markup-url` for an HTTPS PNG annotation URL or `--markup-file` for a local PNG. The annotation must contain transparent pixels and match the first reference after orientation, up to 16,777,216 pixels per image and 40MB for the annotation. With `--image-url`, a local annotation is encoded as a PNG data URL in JSON; with `--image-file`, it is uploaded as a multipart file (an annotation HTTPS URL is also accepted). Markup does not support `file_id` and cannot be combined with mask, GIF or prompt rewriting. GIF frame count is 2–16; frame duration is 20–655350ms, rounded to the nearest 10ms. GIF rejects masks, annotations, custom compression, prompt rewriting and partial streaming. Pricing is unchanged: unsuffixed/`:reverse` models bill per successful file, `:official` bills actual tokens.

```bash
openai-cli edit "Recolor the annotated area" --model gpt-image-2.6-flare \
  --image-file reference.png --markup-file annotation.png --complexity low --async
```
