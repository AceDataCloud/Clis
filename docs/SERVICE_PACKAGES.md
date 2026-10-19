# Find a service package by name

[简体中文](SERVICE_PACKAGES_zh-CN.md)

These are **Ace Data Cloud integrations for the named services**, not official clients from the model owners. The package names, publisher/repository links and observed publication state below were checked on **2026-10-19**. Search ranking and installation in a third-party host are separate checks; a matching name alone is not proof of ownership.

| Service | Ace CLI package | Ace MCP package | Free local check |
|---|---|---|---|
| Suno by Ace Data Cloud | [suno-cli](https://pypi.org/project/suno-cli/) | [mcp-suno](https://pypi.org/project/mcp-suno/) | `suno models` |
| Seedance by Ace Data Cloud | [seedance-cli](https://pypi.org/project/seedance-cli/) | [mcp-seedance](https://pypi.org/project/mcp-seedance/) | `seedance models` |
| HappyHorse by Ace Data Cloud | happyhorse-cli — source only / 未发布 | [mcp-happyhorse](https://pypi.org/project/mcp-happyhorse/) | `happyhorse models` |
| GPT Image by Ace Data Cloud | [openai-pro-cli](https://pypi.org/project/openai-pro-cli/) | [mcp-openai-pro](https://pypi.org/project/mcp-openai-pro/) | `openai-cli image --help` |
| Nano Banana by Ace Data Cloud | [nano-banana-pro-cli](https://pypi.org/project/nano-banana-pro-cli/) | [mcp-nanobanana-pro](https://pypi.org/project/mcp-nanobanana-pro/) | `nano-banana-pro models` |

The ADC CLI contains an offline service-name directory: `adc packages suno`, `adc packages "gpt image" --json`, or `adc packages "nano banana"`. This feature reaches registry users only in a release containing the new command. It does not install packages, change agent settings or make API requests.

## 1. Install the service you need

Open the linked PyPI page, check its source repository is owned by AceDataCloud, and install it in an isolated Python environment. For example:

```bash
python -m pip install suno-cli
suno --help
suno models
```

HappyHorse already has a published MCP. Its CLI remains source-only: [pinned source installation](https://github.com/AceDataCloud/Clis/tree/main/happyhorse). The GPT Image CLI uses the existing `openai-pro-cli`. Its MCP has a separately named service entry, `io.github.AceDataCloud/mcp-gpt-image`, while reusing **mcp-openai-pro>=2026.10.18.2** with **--profile gpt-image**. That profile exposes five image/task tools; it is not a separate PyPI distribution. Preserve the profile arguments instead of substituting the generic OpenAI hosted URL. Do not install the unrelated third-party PyPI package named `mcp-gpt-image`. Follow the [complete service guide](https://github.com/AceDataCloud/OpenAIMCP/blob/main/GPT_IMAGE.md):

```bash
uvx --from 'mcp-openai-pro>=2026.10.18.2' mcp-openai-pro --profile gpt-image
```

Configure your own application key in this server's `ACEDATACLOUD_API_TOKEN` field, then begin with the free static `gpt_image_list_models`. Do not submit a generation for installation validation. The Registry entry does not prove every downstream client's GUI installation. Install separate MCP packages in separate environments, such as each host's `uvx` launcher, because they may share top-level Python module names.

## 2. Register/sign in and create the right API key

1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=cli_catalog_readme_api_key). Register/sign in. If General application does not exist, choose **Initialize General Application**.
2. Copy the application API Key or use **Manage Keys → Create** to create one named for this integration. Check service/model access, expiration, usage limits and account balance against [current pricing](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=cli_catalog_readme_pricing).
3. If **Allowed APIs** is enabled, allow both the generation and task-query operations needed by the service. A query permission alone does not allow generation. Do not substitute a `platform-...` account-management token or a Discord proxy credential.

![Copy an application API key](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/get-api-key-en.png)

![Create a dedicated key](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/create-api-key-en.png)

These are existing, redacted platform screenshots archived in the Suno Dify tutorial (source commit `8d3d0357`). They show only shared key steps, not CLI installation or a new run. The original key-name field says “Dify tutorial”; choose a CLI-specific name yourself.

## 3. Configure this terminal, then use the service

Copy only the raw token, without `Bearer `, quotation marks or spaces. Set `ACEDATACLOUD_API_TOKEN` in the environment launching the CLI; for an MCP host, set it in that server's credential/environment field. Never paste it in prompts, commit it, or expose it in screenshots. Follow your shell's secure input method; no key is needed for `--help` or static reference commands.

Only after checking current access, balance and price should you submit a generation. Keep the returned task ID. Query the same ID using the service README's `task`/`wait` command until terminal; do not regenerate because it is pending. A process exit code or running preview is not final media. Open the returned media link after completion, and inspect the corresponding usage record separately.

| Symptom | Next step |
|---|---|
| 401/403 | Check the full raw token, application/service permissions, expiration and Allowed APIs; do not post the key for support. |
| 400 | Use the exact command/model parameters in that service's current README; services are not interchangeable. |
| Pending / no final URL | Retrieve the same task ID. Do not resubmit generation to poll. |
| 429 | Reduce concurrency and wait; do not silently add paid retries. |
| 5xx / timeout | Inspect the existing task/trace before deciding on another billable attempt. |

## For integration maintainers

Use `service-packages.json` as a service-name-to-owned-package reference. Preserve the source monorepo and edit mirrors through it. Do not infer a dedicated package or ranking from a service alias. The official PyPA [metadata guide](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/) documents summary/keywords/author/source metadata; publish a new version before claiming those edits reached PyPI. UI search evidence and first use need their own dated receipts.
