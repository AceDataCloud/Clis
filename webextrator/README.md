# WebExtrator CLI

A command-line tool for web rendering and extraction via [AceDataCloud](https://platform.acedata.cloud?utm_source=github&utm_medium=referral&utm_campaign=evergreen).

## Get your Ace Data Cloud API key

1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen). Sign in, or register an account first.
2. Open **General Application**. On your first visit, select **Initialize General Application** if prompted. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=github&utm_medium=referral&utm_campaign=evergreen).
3. Click the copy button beside **API KEY**, marked **1** in the screenshot. Store the copied key privately in the `ACEDATACLOUD_API_TOKEN` environment variable on the machine that runs the CLI.
4. Check the service permission, key restrictions and available balance before submitting a request. If your key restricts the allowed APIs, include any generation and task-query operations you plan to use.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy button beside API KEY in General Application, marked 1](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.

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

## Browser and cache options

Both `extract` and `render` default to the server's `load` wait condition. Use
`--wait-until networkidle` only when needed. `--timeout` is a positive integer
navigation timeout in seconds (server default: 30); `--delay` is a nonnegative
integer number of extra seconds.

`--cookies` accepts a JSON array; every cookie needs string `name`, `value` and
`domain` fields. Optional fields include `path`, `expires`, `httpOnly`, `secure`
and `sameSite` (`Strict`, `Lax`, `None`). Use only cookies you are authorized to
send, and avoid putting sensitive values in shared shell history.

`--bypass-cache` skips cache reads but still allows writes. The default cache
lifetime is 3600 seconds; `--cache-ttl-seconds 0` disables writes for that result.

```bash
webextrator render https://example.com --timeout 30 --delay 0 \
  --bypass-cache --cache-ttl-seconds 0 --json
webextrator extract https://example.com \
  --cookies '[{"name":"locale","value":"en","domain":"example.com"}]' --json
```

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
