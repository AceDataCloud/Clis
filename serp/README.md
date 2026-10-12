# SERP CLI

A command-line tool for Google Search (SERP) via the [AceDataCloud](https://platform.acedata.cloud?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=serp_cli_readme_platform) platform.

## Get your Ace Data Cloud API key

1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=serp_cli_readme_api_key). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=serp_cli_readme_pricing).
3. Copy the **API Key** from the application card, or open **Keys / Manage Keys → Create** to create a separate key for this integration. Give it a recognizable name so you can revoke or rotate it independently.
4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Enable only the restrictions you need, allow the operations you will call, then click **Create** and copy the token from the key list. Task lookup does not grant permission to submit a generation. Confirm the application's balance can cover your first request; any trial allowance is whatever your account currently displays.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy an application API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the key in the client's credential store or the environment variable shown below. Never put it in a prompt, shared workflow, screenshot, or Git commit. If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.

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

# Image search with image-size filter
serp images "sunset photography" --image-size 12mp

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
| `--time-range` | Time filter: h, d, w, m, y (or qdr:h, qdr:d, qdr:w, qdr:m, qdr:y) |
| `--image-size` | Image size filter: large, medium, icon, 2mp, 4mp, 6mp, 8mp, 10mp, 12mp, 15mp, 20mp, 40mp, 70mp |
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

- [AceDataCloud Platform](https://platform.acedata.cloud?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=serp_cli_readme_platform)
- [API Documentation](https://platform.acedata.cloud/documents?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=serp_cli_readme_documents)
