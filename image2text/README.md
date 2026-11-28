# Image2Text CLI

A command-line tool for English/numeric captcha recognition via the [AceDataCloud](https://platform.acedata.cloud) API.

## Installation

```bash
pip install image2text-cli
```

## Usage

Sign in to [Applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen) and open **General Application**. On your first visit, select **Initialize General Application** if prompted. Copy the key with the button beside **API KEY**, marked **1** in the screenshot. Store it privately in `ACEDATACLOUD_API_TOKEN` on the machine that runs the CLI.

![Copy button beside API KEY in General Application, marked 1](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

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
