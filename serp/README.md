# SERP CLI

A command-line tool for Google Search (SERP) via the [AceDataCloud](https://platform.acedata.cloud) platform.

## Features

- **Web Search** — Search Google and get structured results (organic, knowledge graph, answer box)
- **Image Search** — Find images with `serp images`
- **News Search** — Get news articles with time filtering
- **Video Search** — Find video content from YouTube and more
- **Places Search** — Find local businesses and places
- **Maps Search** — Search Google Maps for locations
- **Rich Output** — Beautiful terminal formatting with `--json` for scripting
- **Localization** — Country and language support for localized results

## Installation

```bash
pip install serp-cli
```

## Quick Start

```bash
# Set your API token
export ACEDATACLOUD_API_TOKEN=your_token_here

# Web search
serp search "artificial intelligence"

# Image search
serp images "sunset photography"

# News with time filter
serp news "tech news" --time-range qdr:d

# Places search
serp places "coffee shops near Times Square" -c us

# Search with pagination
serp search "python tutorials" -n 20 -p 2

# Get JSON output
serp search "hello world" --json | jq '.organic[0].title'
```

## Commands

| Command | Description |
|---------|-------------|
| `search` | Google web search (all types via `-t`) |
| `images` | Google Image search |
| `news` | Google News search |
| `videos` | Google Video search |
| `places` | Google Places search |
| `maps` | Google Maps search |
| `search-types` | List available search types |
| `time-ranges` | List time range filters |
| `config` | Show current configuration |

## Search Options

| Option | Description |
|--------|-------------|
| `-t`, `--type` | Search type: search, images, news, maps, places, videos |
| `-c`, `--country` | Country code (e.g. us, cn, uk) |
| `-l`, `--language` | Language code (e.g. en, zh-cn, fr) |
| `--time-range` | Time filter: qdr:h (hour), qdr:d (day), qdr:w (week), qdr:m (month) |
| `-n`, `--number` | Number of results per page (default: 10) |
| `-p`, `--page` | Page number for pagination |
| `--json` | Output raw JSON |

## Configuration

| Environment Variable | Description | Default |
|---------------------|-------------|---------|
| `ACEDATACLOUD_API_TOKEN` | API authentication token | (required) |
| `ACEDATACLOUD_API_BASE_URL` | API base URL | `https://api.acedata.cloud` |
| `SERP_REQUEST_TIMEOUT` | Request timeout in seconds | `30` |

You can also use a `.env` file or pass `--token` directly.

## Docker

```bash
docker compose run serp-cli search "hello world"
```

## Development

```bash
# Install with dev dependencies
pip install -e ".[all]"

# Run tests
pytest

# Run linter
ruff check .
ruff format --check .
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Links

- [AceDataCloud Platform](https://platform.acedata.cloud)
- [API Documentation](https://docs.acedata.cloud)
