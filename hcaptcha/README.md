# hCaptcha CLI

A command-line tool for hCaptcha verification via the [AceDataCloud](https://platform.acedata.cloud) API.

## Installation

```bash
pip install hcaptcha-cli
```

## Usage

```bash
# Set your API token
export ACEDATACLOUD_API_TOKEN=your_token

# Recognize hCaptcha images
hcaptcha recognize --queries '["https://example.com/img.jpg"]' --question "Select all cars"

# Recognize hCaptcha images asynchronously
hcaptcha recognize --queries '["https://example.com/img.jpg"]' --async

# Get a hCaptcha bypass token
hcaptcha token <website_key> <website_url>

# Get token asynchronously
hcaptcha token <website_key> <website_url> --async

# Show configuration
hcaptcha config
```

## Commands

- `recognize` — Classify hCaptcha challenge images
- `token` — Solve hCaptcha and retrieve a token
- `config` — Show current configuration

## Authentication

Get your API token at [https://platform.acedata.cloud](https://platform.acedata.cloud).

Pass the token via `--token` flag or set the `ACEDATACLOUD_API_TOKEN` environment variable.
