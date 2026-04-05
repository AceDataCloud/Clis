# Wan CLI

A command-line interface for [Tongyi Wansiang](https://platform.acedata.cloud) AI Video Generation via the AceDataCloud API.

## Installation

```bash
pip install wan-cli
```

## Setup

Get your API token from [AceDataCloud Platform](https://platform.acedata.cloud).

```bash
export ACEDATACLOUD_API_TOKEN=your_token_here
```

Or copy `.env.example` to `.env` and set your token.

## Usage

### Generate a video from text

```bash
wan generate "Astronauts shuttle from space to volcano"
wan generate "A cat playing in the garden" -m wan2.6-t2v -r 720P
wan generate "Ocean waves" -d 10 --shot-type single
```

### Generate a video from an image

```bash
wan image-to-video "Animate this scene" -i https://example.com/photo.jpg
wan image-to-video "Bring to life" -i https://cdn.acedata.cloud/r9vsv9.png -m wan2.6-i2v
```

### Generate a video from a reference video

```bash
wan reference-to-video "A person dancing" --reference-video-urls https://example.com/ref.mp4
```

### Query task status

```bash
wan task abc123-def456
wan tasks abc123 def456 ghi789
```

### Wait for task completion

```bash
wan wait abc123
wan wait abc123 --interval 10 --timeout 300
```

### View available options

```bash
wan models
wan resolutions
wan shot-types
wan config
```

## Options

### Global options

- `--token`: API token (or set `ACEDATACLOUD_API_TOKEN`)
- `--json`: Output raw JSON

### Generate options

- `-m, --model`: Model version (`wan2.6-t2v`, `wan2.6-i2v`, `wan2.6-i2v-flash`, `wan2.6-r2v`)
- `-r, --resolution`: Output resolution (`480P`, `720P`, `1080P`)
- `-d, --duration`: Video duration in seconds (`5`, `10`, `15`)
- `--shot-type`: Shot type (`single`, `multi`)
- `--negative-prompt`: Content to exclude from video
- `--audio/--no-audio`: Enable/disable audio in video
- `--prompt-extend/--no-prompt-extend`: Enable intelligent prompt rewriting
- `--callback-url`: Webhook callback URL

## Models

| Model | Type | Description |
|-------|------|-------------|
| `wan2.6-t2v` | Text-to-Video | Generate video from text prompt (default) |
| `wan2.6-i2v` | Image-to-Video | Generate video from image |
| `wan2.6-i2v-flash` | Image-to-Video Fast | Fast image-to-video generation |
| `wan2.6-r2v` | Reference-to-Video | Generate video using reference video |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ACEDATACLOUD_API_TOKEN` | _(required)_ | Your AceDataCloud API token |
| `ACEDATACLOUD_API_BASE_URL` | `https://api.acedata.cloud` | API base URL |
| `WAN_DEFAULT_MODEL` | `wan2.6-t2v` | Default model |
| `WAN_REQUEST_TIMEOUT` | `1800` | Request timeout in seconds |

## License

MIT License - see [LICENSE](LICENSE) for details.
