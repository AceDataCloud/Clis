# GLM CLI

A command-line tool for GLM chat completions via [AceDataCloud](https://platform.acedata.cloud?utm_source=pypi&utm_medium=referral&utm_campaign=evergreen).

## Get your Ace Data Cloud API key

1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=pypi&utm_medium=referral&utm_campaign=evergreen). Sign in, or register an account first.
2. Open **General Application**. On your first visit, select **Initialize General Application** if prompted. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=pypi&utm_medium=referral&utm_campaign=evergreen).
3. Click the copy button beside **API KEY**, marked **1** in the screenshot. Store the copied key privately in the `ACEDATACLOUD_API_TOKEN` environment variable on the machine that runs the CLI.
4. Check the service permission, key restrictions and available balance before submitting a request. If your key restricts the allowed APIs, include any generation and task-query operations you plan to use.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy button beside API KEY in General Application, marked 1](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.

## Installation

```bash
pip install glm-pro-cli
```

## Quick Start

```bash
export ACEDATACLOUD_API_TOKEN=your_token

glm chat "What is the capital of France?"
glm chat "Explain AI" -m glm-5.3
glm models
```

## Commands

| Command | Description |
|---------|-------------|
| `glm chat <prompt>` | Chat with a GLM model |
| `glm models` | List available GLM models |
| `glm config` | Show current configuration |

## Global Options

```
--token TEXT    API token (or set ACEDATACLOUD_API_TOKEN env var)
--version       Show version
--help          Show help message
```

## Available Models

| Model | Notes |
|-------|-------|
| `glm-5.3` | Latest GLM release |
| `glm-5.2` | GLM-5 series |
| `glm-5` | GLM-5 base model |
| `glm-5-turbo` | GLM-5 Turbo |
| `glm-5.1` | Earlier GLM-5 release |
| `glm-4.7` | GLM-4 series (default) |
| `glm-4.6` | GLM-4 series |
| `glm-4.5` | GLM-4 series |
| `glm-4.5v` | Vision-capable GLM-4 model |
| `glm-3-turbo` | GLM-3 Turbo |

## Configuration

Set environment variables or use a `.env` file:

```bash
ACEDATACLOUD_API_TOKEN=your_token
ACEDATACLOUD_API_BASE_URL=https://api.acedata.cloud
GLM_REQUEST_TIMEOUT=30
```

## License

MIT
