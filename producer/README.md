# Producer CLI

A command-line tool for AI music generation using the Producer service via AceDataCloud API.

## Get your Ace Data Cloud API key

1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=producer_cli_readme_api_key). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=producer_cli_readme_pricing).
3. Copy the **API Key** from the application card, or open **Keys / Manage Keys → Create** to create a separate key for this integration. Give it a recognizable name so you can revoke or rotate it independently.
4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Enable only the restrictions you need, allow the operations you will call, then click **Create** and copy the token from the key list. Task lookup does not grant permission to submit a generation. Confirm the application's balance can cover your first request; any trial allowance is whatever your account currently displays.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy an application API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the key in the client's credential store or the environment variable shown below. Never put it in a prompt, shared workflow, screenshot, or Git commit. If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.

## Installation

```bash
pip install producer-cli
```

## Usage

```bash
# Set your API token
export ACEDATACLOUD_API_TOKEN=your_token

# Generate a music track
producer generate "A happy upbeat pop song about summer"

# Generate with a specific model
producer generate "Dark metal with heavy guitar riffs" -m "FUZZ-2.0 Pro"

# Generate an instrumental track
producer generate "Epic orchestral battle theme" --instrumental

# Generate lyrics
producer lyrics "A love song about the ocean at sunset"

# Create a cover of an existing track
producer cover abc123-def456

# Extend an existing track
producer extend abc123-def456 --continue-at 30.5

# Generate a variation
producer variation abc123-def456

# Swap vocals
producer swap-vocals abc123-def456

# Swap instrumentals
producer swap-instrumentals abc123-def456

# Replace a section
producer replace-section abc123 --replace-section-start 10 --replace-section-end 30

# Extract stems
producer stems abc123-def456

# Upload audio from URL
producer upload https://example.com/my-audio.mp3

# Generate video from audio
producer video abc123-def456

# Get WAV format
producer wav abc123-def456

# Check task status
producer task abc123-def456

# Wait for task completion
producer wait abc123-def456

# List available models
producer models

# Show configuration
producer config
```

## Authentication

Set your API token via the `ACEDATACLOUD_API_TOKEN` environment variable or use the `--token` option:

```bash
producer --token your_token generate "A happy song"
```

## License

MIT
