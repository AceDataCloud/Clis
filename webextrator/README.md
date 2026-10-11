# WebExtrator CLI

A command-line tool for web rendering and extraction via [AceDataCloud](https://platform.acedata.cloud?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=webextrator_cli_readme_platform).

## Get your Ace Data Cloud API key

1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=webextrator_cli_readme_api_key). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=webextrator_cli_readme_pricing).
3. Copy the **API Key** from the application card, or open **Keys / Manage Keys → Create** to create a separate key for this integration. Give it a recognizable name so you can revoke or rotate it independently.
4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Enable only the restrictions you need, allow the operations you will call, then click **Create** and copy the token from the key list. Task lookup does not grant permission to submit a generation. Confirm the application's balance can cover your first request; any trial allowance is whatever your account currently displays.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy an application API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the key in the client's credential store or the environment variable shown below. Never put it in a prompt, shared workflow, screenshot, or Git commit. If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.

## Installation

```bash
pip install webextrator-cli
```

## Quick Start

```bash
export ACEDATACLOUD_API_TOKEN=your_token

webextrator extract https://www.amazon.com/dp/B0C1234567
webextrator render https://example.com
webextrator tasks retrieve --id <task-id>
```

## Commands

| Command | Description |
|---------|-------------|
| `webextrator extract <url>` | Extract structured content from a web page |
| `webextrator render <url>` | Render a web page and return the HTML |
| `webextrator tasks retrieve` | Retrieve a single task by ID or trace ID |
| `webextrator tasks batch` | Retrieve multiple tasks at once |
| `webextrator config` | Show current configuration |

## Global Options

```
--token TEXT    API token (or set ACEDATACLOUD_API_TOKEN env var)
--version       Show version
--help          Show help message
```

## Configuration

Set environment variables or use a `.env` file:

```bash
ACEDATACLOUD_API_TOKEN=your_token
ACEDATACLOUD_API_BASE_URL=https://api.acedata.cloud
WEBEXTRATOR_REQUEST_TIMEOUT=60
```

## License

MIT
