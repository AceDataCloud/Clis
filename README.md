# AceDataCloud CLIs

Monorepo for all AceDataCloud command-line interface tools.

## Get your Ace Data Cloud API key

1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=cli_catalog_readme_api_key). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=cli_catalog_readme_pricing).
3. Copy the **API Key** from the application card, or open **Keys / Manage Keys → Create** to create a separate key for this integration. Give it a recognizable name so you can revoke or rotate it independently.
4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Enable only the restrictions you need, allow the operations you will call, then click **Create** and copy the token from the key list. Task lookup does not grant permission to submit a generation. Confirm the application's balance can cover your first request; any trial allowance is whatever your account currently displays.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy an application API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the key in the client's credential store or the environment variable shown below. Never put it in a prompt, shared workflow, screenshot, or Git commit. If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.

## CLIs

| Directory | Standalone Repo | Description |
|---|---|---|
| `luma/` | [LumaCli](https://github.com/AceDataCloud/LumaCli) | Luma video generation CLI |
| `suno/` | [SunoCli](https://github.com/AceDataCloud/SunoCli) | Suno music generation CLI |
| `sora/` | [SoraCli](https://github.com/AceDataCloud/SoraCli) | Sora video generation CLI |
| `veo/` | [VeoCli](https://github.com/AceDataCloud/VeoCli) | Veo video generation CLI |
| `nanobanana/` | [NanoBananaCli](https://github.com/AceDataCloud/NanoBananaCli) | NanoBanana image generation CLI |
| `seedance/` | [SeedanceCli](https://github.com/AceDataCloud/SeedanceCli) | Seedance video generation CLI |
| `seedream/` | [SeedreamCli](https://github.com/AceDataCloud/SeedreamCli) | Seedream image generation CLI |
| `flux/` | [FluxCli](https://github.com/AceDataCloud/FluxCli) | Flux image generation & editing CLI |
| `serp/` | [SerpCli](https://github.com/AceDataCloud/SerpCli) | Google SERP (Search) CLI |
| `wan/` | [WanCli](https://github.com/AceDataCloud/WanCli) | Tongyi Wansiang video generation CLI |
| `adc/` | [AceDataCloudCli](https://github.com/AceDataCloud/AceDataCloudCli) | Unified AceDataCloud CLI (all services) |
| `aichat/` | [AiChatCli](https://github.com/AceDataCloud/AiChatCli) | AI Dialogue CLI |
| `glm/` | [GLMCli](https://github.com/AceDataCloud/GLMCli) | GLM chat completions CLI |
| `hailuo/` | [HailuoCli](https://github.com/AceDataCloud/HailuoCli) | Hailuo video generation CLI |
| `kling/` | [KlingCli](https://github.com/AceDataCloud/KlingCli) | Kling video generation CLI |
| `openai/` | [OpenAICli](https://github.com/AceDataCloud/OpenAICli) | OpenAI-compatible API CLI |
| `producer/` | [ProducerCli](https://github.com/AceDataCloud/ProducerCli) | Producer music generation CLI |
| `webextrator/` | [WebExtratorCli](https://github.com/AceDataCloud/WebExtratorCli) | Web extraction and rendering CLI |

## How It Works

This is the source-of-truth monorepo. Changes pushed to `main` are automatically synced to the standalone repos via GitHub Actions.

The mapping between subdirectories and standalone repos is defined in [`sync.yaml`](sync.yaml).

**Do not edit standalone repos directly** — all changes should be made here.

## Contract updates

PlatformBackend's daily ecosystem CronJob prepares incremental capability PRs
using a pinned Backend source. Existing CI and human review gate each update.
The previous dispatch/Copilot sync workflows are retired.

## Test discovery

The ADC Docker build runs `pytest`.
Tests requiring real API credentials must use `pytest.mark.integration`;
their filenames do not need to be listed in the Dockerfile. Other CLI packages
continue to use their existing automatic pytest discovery.

## Daily capability updates

PlatformBackend `ecosystem.py` is the only scheduled coordinator.
One daily Kubernetes Job reviews Backend docs and API changes with Claude Code,
updates existing files, and creates or updates one reviewable PR per repository.
It never merges PRs or duplicates the Backend guide tree. Normal CI and review
remain required; publication and sub-repository mirroring run after merge.
