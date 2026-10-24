# Kling CLI

A command-line tool for Kling AI Video Generation via [AceDataCloud](https://platform.acedata.cloud?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=kling_cli_readme_platform).

## Get your Ace Data Cloud API key

1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=kling_cli_readme_api_key). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=kling_cli_readme_pricing).
3. Copy the **API Key** from the application card, or open **Keys / Manage Keys → Create** to create a separate key for this integration. Give it a recognizable name so you can revoke or rotate it independently.
4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Enable only the restrictions you need, allow the operations you will call, then click **Create** and copy the token from the key list. Task lookup does not grant permission to submit a generation. Confirm the application's balance can cover your first request; any trial allowance is whatever your account currently displays.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy an application API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the key in the client's credential store or the environment variable shown below. Never put it in a prompt, shared workflow, screenshot, or Git commit. If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.

## Installation

```bash
pip install kling-pro-cli
```

## Usage

```bash
# Set your API token
export ACEDATACLOUD_API_TOKEN=your_token

# Generate a video from a text prompt
kling generate "A cinematic scene of a sunset over the ocean"

# Generate a video from a reference image
kling image-to-video "Animate this scene" --start-image-url https://example.com/photo.jpg

# Extend an existing video
kling extend --video-id abc123

# Generate a motion video from image + reference video
kling motion --image-url https://example.com/img.jpg --video-url https://example.com/ref.mp4

# Check task status
kling task abc123-def456

# Wait for a task to complete
kling wait abc123 --interval 5

# List available models
kling models

# Show configuration
kling config
```

## Options

- `--token` / `ACEDATACLOUD_API_TOKEN` — API token
- `--json` — Output raw JSON

## Models

| Model | Notes |
|-------|-------|
| kling-v1 | Default model |
| kling-v1-6 | Version 1.6 |
| kling-v2-5-turbo | Version 2.5 Turbo |
| kling-v2-6 | Version 2.6 |
| kling-v3 | Version 3 (supports 4K mode) |
| kling-v3-omni | Version 3 Omni (supports 4K mode) |
| kling-o1 | Video O1 |
| kling-v2-master | Version 2 Master |
| kling-v2-1-master | Version 2.1 Master |

## License

MIT

## Native video and commerce

`kling turbo --request-file request.json` accepts `{"prompt":"Waves at sunset","duration":7}`. V3 Turbo supports std 720p/pro 1080p and integer durations 3–15 seconds; native audio is included and cannot be disabled.

`kling storyboard --request-file request.json` supports V3/V3 Omni automatic or custom multishot generation. For custom shots use `shot_type="customize"`, total `duration`, and `multi_prompt` with 1–6 consecutive indices and durations summing to the total.

Use `apparel`, `goods-studio`, `video-commerce` and `virtual-try-on` with `--request-file` for structured contents/settings. Product studio requires ref_image and goods_title, an aspect ratio and duration 15/30/60. Try-on requires product_image and person_image URLs. Creator video needs one avatar and a speech_script. Commands output JSON and submit asynchronously by default; use existing task/wait commands for final delivery, or set `async=false` in the request. Billing follows the selected tier and actual output duration or image count.

## Reference inputs

Use `element_list` and `voice_list` only with already valid platform references and the supported model combinations in the current backend guide. Standalone asset creation and management are not published.

### O1 and Omni reference-video billing

For `generate` or `image-to-video` with `kling-o1` or `kling-v3-omni`, pass at most one reference video through `--video-list` and use `--no-generate-audio`. Reference videos use a separate billing tier: **1.202 Credits per billed second** in `std`, or **1.602 Credits per billed second** in `pro`. Reference images (`--image-list`, start/end frames) alone do not trigger this tier.

For a 5-second `kling-o1` output:

| Mode | Without reference video | With reference video (5 billed seconds) |
|---|---:|---:|
| std | 4.005 Credits | 6.010 Credits |
| pro | 5.340 Credits | 8.010 Credits |

With `refer_type=base` (the default), editing may follow the reference video's length, and billing uses actual output duration rounded to whole seconds (5.708 seconds bills as 6; 5.041 bills as 5). With `refer_type=feature`, billing uses the requested `--duration`. Use `--json` to inspect `usage.reference_video_seconds` for final billed seconds; an estimate at submission can differ from the final charge. Do not submit this response field as a request parameter.

```bash
kling generate 'Restyle <<<video_1>>> as a watercolor animation' \
  --model kling-o1 --mode std --no-generate-audio \
  --video-list '[{"video_url":"https://example.com/ref.mp4","refer_type":"base"}]' --json
```

Reference videos cannot be combined with audio generation. `base` references also cannot be combined with start/end frames; use `feature` for compatible frame-based requests.
