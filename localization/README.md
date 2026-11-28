# Localization CLI

A command-line tool for localization translation via the [AceDataCloud](https://platform.acedata.cloud) API.

## Installation

```bash
pip install localization-cli
```

## Usage

```bash
export ACEDATACLOUD_API_TOKEN=your_token

# Translate markdown content
localization translate "# Title 1" --locale zh-CN

# Translate a JSON localization object
localization translate '{"message.clickButton":{"message":"Please click button to apply"}}' --extension json --locale zh-CN
```

## Configuration

Set your API token as an environment variable:

```bash
export ACEDATACLOUD_API_TOKEN=your_token
```

Or pass it directly:

```bash
localization --token your_token translate "# Title 1" --locale zh-CN
```
