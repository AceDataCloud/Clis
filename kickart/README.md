# Kickart CLI

A command-line tool for Kickart e-commerce video generation via the [AceDataCloud](https://platform.acedata.cloud) API.

## Installation

```bash
pip install kickart-cli
```

## Usage

```bash
export ACEDATACLOUD_API_TOKEN=your_token

# Generate an e-commerce video
kickart video --duration 15 --product-url https://example.com/product

# Generate a viral video
kickart viral-video --ref-video https://example.com/ref.mp4 --language en

# Generate a template video
kickart template-video --template-id tmpl_123 --resource '[{"type":"image","url":"https://example.com/img.jpg"}]'
```

## Configuration

Set your API token as an environment variable:

```bash
export ACEDATACLOUD_API_TOKEN=your_token
```
