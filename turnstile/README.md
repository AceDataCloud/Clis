# Cloudflare Turnstile CLI

A command-line tool for Cloudflare Turnstile captcha bypass via the [AceDataCloud](https://platform.acedata.cloud) API.

## Installation

```bash
pip install turnstile-cli
```

## Usage

Sign in to [Applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen) and open **General Application**. On your first visit, select **Initialize General Application** if prompted. Copy the key with the button beside **API KEY**, marked **1** in the screenshot. Store it privately in `ACEDATACLOUD_API_TOKEN` on the machine that runs the CLI.

![Copy button beside API KEY in General Application, marked 1](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

```bash
# Set your API token
export ACEDATACLOUD_API_TOKEN=your_token

# Get a Turnstile bypass token
turnstile token <website_key> <website_url>

# Get token with action
turnstile token <website_key> <website_url> --action login

# Get token with cdata
turnstile token <website_key> <website_url> --cdata some-cdata

# Get token asynchronously
turnstile token <website_key> <website_url> --async

# Show configuration
turnstile config
```

## Commands

- `token` — Solve Cloudflare Turnstile and retrieve a token
- `config` — Show current configuration

## Authentication

Get your API token at [https://platform.acedata.cloud](https://platform.acedata.cloud).

Pass the token via `--token` flag or set the `ACEDATACLOUD_API_TOKEN` environment variable.
