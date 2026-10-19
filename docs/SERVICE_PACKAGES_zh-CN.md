# 按服务名找到正确安装包

[English](SERVICE_PACKAGES.md)

以下是 **Ace Data Cloud 提供的服务集成**，不是模型方官方客户端。包名、源码身份与发布状态核验日为 **2026-10-19**；搜索排名、具体宿主安装和真实生成需分别验证，同名第三方包不能当 Ace 收录。

| 服务 | Ace CLI 包 | Ace MCP 包 | 本地免费检查 |
|---|---|---|---|
| Suno by Ace Data Cloud | [suno-cli](https://pypi.org/project/suno-cli/) | [mcp-suno](https://pypi.org/project/mcp-suno/) | `suno models` |
| Seedance by Ace Data Cloud | [seedance-cli](https://pypi.org/project/seedance-cli/) | [mcp-seedance](https://pypi.org/project/mcp-seedance/) | `seedance models` |
| HappyHorse by Ace Data Cloud | happyhorse-cli — source only / 未发布 | [mcp-happyhorse](https://pypi.org/project/mcp-happyhorse/) | `happyhorse models` |
| GPT Image by Ace Data Cloud | [openai-pro-cli](https://pypi.org/project/openai-pro-cli/) | [mcp-openai-pro](https://pypi.org/project/mcp-openai-pro/) | `openai-cli image --help` |
| Nano Banana by Ace Data Cloud | [nano-banana-pro-cli](https://pypi.org/project/nano-banana-pro-cli/) | [mcp-nanobanana-pro](https://pypi.org/project/mcp-nanobanana-pro/) | `nano-banana-pro models` |

ADC CLI 中新增离线服务目录：`adc packages suno`、`adc packages "gpt image" --json`、`adc packages "nano banana"`。需要发布包含该命令的新版本后，registry 用户才可用；它不会安装包、修改 Agent 配置或请求 API。

## 1. 安装具体服务

先点包页面，核对源码归属 AceDataCloud，在隔离 Python 环境安装。例如：

```bash
python -m pip install suno-cli
suno --help
suno models
```

HappyHorse 已有公开 MCP；CLI 仍为源码安装，不能用未发布包的 `pip install happyhorse-cli`。GPT Image CLI 使用现有 `openai-pro-cli`。MCP 已有独立品牌工具入口：官方 Registry 名称 `io.github.AceDataCloud/mcp-gpt-image`，复用 **mcp-openai-pro>=2026.10.18.2** 并保留 **--profile gpt-image**，只展示五个图像/任务工具；这不是新PyPI包。不要用泛OpenAI托管地址代替它，也不要把第三方PyPI同名 `mcp-gpt-image` 当Ace包。按[完整GPT Image指南](https://github.com/AceDataCloud/OpenAIMCP/blob/main/GPT_IMAGE.md)配置：

```bash
uvx --from 'mcp-openai-pro>=2026.10.18.2' mcp-openai-pro --profile gpt-image
```

把本机自己的应用Key放入宿主该server的 `ACEDATACLOUD_API_TOKEN`，先用免费静态 `gpt_image_list_models`，不发生成。独立Registry收录不代表所有下游客户端GUI安装已验。MCP 包可能共用顶层 Python 模块，请使用宿主的独立 `uvx` 环境，不要把多个包直接混装到同一环境运行。

## 2. 注册/登录并取得正确的 API Key

1. 打开 [Ace Data Cloud → Applications / 我的应用](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=cli_catalog_readme_api_key)，注册或登录；没有通用应用时点击 **Initialize General Application / 初始化通用应用**。
2. 复制应用 API Key，或进 **Manage Keys / 管理密钥 → Create / 创建**，给本次集成命名。检查服务和模型权限、有效期、用量限制及余额，再核对[当前价格](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=cli_catalog_readme_pricing)。
3. 如果启用 **Allowed APIs / 允许的接口**，同时允许该服务所需生成和任务查询接口；查询权限不等于生成权限。不要用平台管理 Token 或 Discord 代理凭据代替生成 Key。

![Copy an application API key](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/get-api-key-en.png)

![Create a dedicated key](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/create-api-key-en.png)

原图来自 Suno Dify 教程固定提交 `8d3d0357`，真实敏感值已遮挡；仅展示通用密钥步骤，不证明 CLI 安装或新调用。原图名称是 Dify tutorial，实际请填写自己的 CLI 名称。

## 3. 配置当前终端，再使用服务

只复制原始 Token，不加 Bearer、引号或空格。在启动 CLI 的环境设置 `ACEDATACLOUD_API_TOKEN`；MCP 则填到宿主该服务器的凭据/环境变量位置。不要放提示词、Git 或截图；使用自己 shell 的安全输入方式。查看 --help 和静态参考列表不需要 Key。

确认权限、余额和当前价后才提交生成。保存返回的 task ID，按服务 README 的 task/wait 命令查询**同一个 ID**到最终状态；pending 不能靠重复生成解决。进程退出成功、运行中的预览均不代表最终媒体，完成后打开返回链接，再独立核对使用账单。

| 问题 | 操作 |
|---|---|
| 401/403 | 检查完整原始Key、应用/服务权限、有效期及Allowed APIs，不把Key发给支持。 |
| 400 | 核对该服务当前README的准确命令、模型和参数，不混用不同服务字段。 |
| pending或无结果URL | 查询原task ID，不重新生成来轮询。 |
| 429 | 等待、降低并发，不悄悄增加付费重试。 |
| 5xx/超时 | 先查原任务/trace，再决定是否重新发起收费操作。 |

## 给集成维护者

复用 service-packages.json 的服务名到真实Ace包映射，修改单一源码再镜像，不据别名臆造独立包或搜索排名。官方[PyPA元数据规范](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)说明summary/keywords/author/source字段；修改后需发布新版本再读包页。搜索截图和真实首调独立留日期回执。
