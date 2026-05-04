# WebExtrator CLI

A command-line tool for web rendering and extraction via [AceDataCloud](https://platform.acedata.cloud).

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
