# Localization CLI

A command-line tool for localization translation via the [AceDataCloud](https://platform.acedata.cloud) API.

## Installation

```bash
pip install localization-cli
```

## Usage

Sign in to [Applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen) and open **General Application**. On your first visit, select **Initialize General Application** if prompted. Copy the key with the button beside **API KEY**, marked **1** in the screenshot. Store it privately in `ACEDATACLOUD_API_TOKEN` on the machine that runs the CLI.

![Copy button beside API KEY in General Application, marked 1](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

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
