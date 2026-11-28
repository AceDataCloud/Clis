# Kickart CLI

A command-line tool for Kickart e-commerce video generation via the [AceDataCloud](https://platform.acedata.cloud) API.

## Installation

```bash
pip install kickart-cli
```

## Usage

Sign in to [Applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen) and open **General Application**. On your first visit, select **Initialize General Application** if prompted. Copy the key with the button beside **API KEY**, marked **1** in the screenshot. Store it privately in `ACEDATACLOUD_API_TOKEN` on the machine that runs the CLI.

![Copy button beside API KEY in General Application, marked 1](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

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
