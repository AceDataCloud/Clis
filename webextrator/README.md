# WebExtrator CLI

A command-line tool for WebExtrator Web Render & Extract via AceDataCloud API.

## Installation

```bash
pip install webextrator-cli
```

## Setup

```bash
export ACEDATACLOUD_API_TOKEN=your_token_here
```

Or copy `.env.example` to `.env` and fill in your token.

## Usage

```bash
webextrator extract https://www.amazon.com/dp/B0C1234567
webextrator render https://example.com
webextrator tasks retrieve --id <task-id>
webextrator config
```

## Commands

| Command | Description |
|---------|-------------|
| `webextrator extract <url>` | Extract structured content from a web page |
| `webextrator render <url>` | Render a web page and return the rendered HTML |
| `webextrator tasks retrieve` | Retrieve a single async task by ID or trace ID |
| `webextrator tasks batch` | Retrieve multiple async tasks at once |
| `webextrator config` | Show current configuration |

## Extract Options

| Option | Description |
|--------|-------------|
| `--expected-type` | Page type hint: product, article, general |
| `--enable-llm` | Enable LLM-based semantic normalization |
| `--wait-until` | Page load wait condition: load, domcontentloaded, networkidle, commit |
| `--timeout` | Total timeout in seconds (default: 30) |
| `--delay` | Extra delay after page load, before extraction |
| `--wait-for-selector` | CSS selector to wait for before extraction |
| `--block-resource` | Resource types to block: image, font, media, stylesheet, xhr, fetch |
| `--user-agent` | Override the User-Agent header |
| `--callback-url` | Webhook URL for async processing |
| `--json` | Output raw JSON |

## Render Options

| Option | Description |
|--------|-------------|
| `--wait-until` | Page load wait condition |
| `--timeout` | Total timeout in seconds (default: 30) |
| `--delay` | Extra delay after page load |
| `--wait-for-selector` | CSS selector to wait for |
| `--block-resource` | Resource types to block (repeatable) |
| `--user-agent` | Override the User-Agent header |
| `--callback-url` | Webhook URL for async processing |
| `--json` | Output raw JSON |

## License

MIT
