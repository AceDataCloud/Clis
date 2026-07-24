# Cloudflare Turnstile CLI

A command-line tool for Cloudflare Turnstile captcha bypass via the [AceDataCloud](https://platform.acedata.cloud) API.

## Installation

```bash
pip install turnstile-cli
```

## Usage

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
