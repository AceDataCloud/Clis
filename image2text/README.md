# Image2Text CLI

A command-line tool for recognizing text from captcha images via the [AceDataCloud](https://platform.acedata.cloud) API.

## Installation

```bash
pip install image2text-cli
```

## Usage

```bash
# Set your API token
export ACEDATACLOUD_API_TOKEN=your_token

# Recognize text from a captcha image (base64)
image2text recognize /9j/4AAQSkZJRgAB...

# Recognize asynchronously
image2text recognize /9j/4AAQSkZJRgAB... --async

# Output raw JSON
image2text recognize /9j/4AAQSkZJRgAB... --json

# Show configuration
image2text config
```

## API Endpoints

- `POST /captcha/recognition/image2text` — Recognize English/numerical text from captcha images

## License

MIT
