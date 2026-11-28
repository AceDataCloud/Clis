# Image2Text CLI

A command-line tool for English/numeric captcha recognition via the [AceDataCloud](https://platform.acedata.cloud) API.

## Installation

```bash
pip install image2text-cli
```

## Usage

```bash
export ACEDATACLOUD_API_TOKEN=your_token

# Recognize text from an image
image2text recognize https://example.com/captcha.png

# Async mode
image2text recognize https://example.com/captcha.png --async
```

## Configuration

Set your API token as an environment variable:

```bash
export ACEDATACLOUD_API_TOKEN=your_token
```

Or pass it directly:

```bash
image2text --token your_token recognize https://example.com/captcha.png
```
