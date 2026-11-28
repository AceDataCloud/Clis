# hCaptcha CLI

A command-line tool for hCaptcha verification via the [AceDataCloud](https://platform.acedata.cloud) API.

## Installation

```bash
pip install hcaptcha-cli
```

## Usage

Sign in to [Applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen) and open **General Application**. On your first visit, select **Initialize General Application** if prompted. Copy the key with the button beside **API KEY**, marked **1** in the screenshot. Store it privately in `ACEDATACLOUD_API_TOKEN` on the machine that runs the CLI.

![Copy button beside API KEY in General Application, marked 1](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

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

# Get token using a proxy
hcaptcha token <website_key> <website_url> --proxy http://127.0.0.1:8080

# Get token with hCaptcha rqdata
hcaptcha token <website_key> <website_url> --rqdata <rqdata>

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
