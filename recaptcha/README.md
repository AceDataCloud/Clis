# reCAPTCHA CLI

A command-line tool for reCAPTCHA verification via the [AceDataCloud](https://platform.acedata.cloud) API.

## Installation

```bash
pip install recaptcha-cli
```

## Usage

```bash
export ACEDATACLOUD_API_TOKEN=your_token

# Recognize reCAPTCHA v2 image
recaptcha recognize2 https://example.com/captcha.jpg "Select all cars"

# Get reCAPTCHA v2 token
recaptcha token2 <site-key> https://example.com

# Get reCAPTCHA v3 token
recaptcha token3 <site-key> https://example.com --page-action submit
```

## Configuration

Set your API token as an environment variable:

```bash
export ACEDATACLOUD_API_TOKEN=your_token
```
