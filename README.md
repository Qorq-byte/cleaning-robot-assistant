# 清洁机器人售后助手

一个面向扫地机器人 / 扫拖一体机器人的智能客服项目：基于 **LangChain ReAct Agent + RAG（检索增强生成）** 构建，通过 Streamlit 提供 Web 对话界面，可回答产品使用、故障排查、选购指南、维护保养等问题，并支持生成个人使用情况报告。

> 页面标题：祺orQ的机器人智能客服

## 功能特性

- **智能问答**：结合知识库回答扫地/扫拖机器人相关问题，支持连续多轮对话与流式输出。
- **RAG 知识检索**：将 `data/` 下的 txt / pdf 知识文档切分后存入 Chroma 向量库，回答前自动检索相关资料。
- **ReAct 工具调用**：Agent 按“思考 → 行动 → 观察 → 再思考”的流程自主调用工具获取信息。
- **报告生成场景**：通过动态提示词切换进入报告写作模式，根据用户 ID 与月份查询使用记录并生成报告。
- **工具监控与日志**：通过中间件记录工具调用、模型请求等信息。

## 技术栈

| 类别 | 说明 |
| --- | --- |
| Web UI | [Streamlit](https://streamlit.io/) |
| Agent 框架 | LangChain / langgraph |
| 大模型 | 通义千问（`ChatTongyi`，默认模型 `qwen3-max`） |
| Embedding | DashScope（默认模型 `text-embedding-v4`） |
| 向量数据库 | Chroma |
| 文档加载 | txt / PDF |
| 配置 | YAML |

## 项目结构

```text
.
├─ app.py                      # Streamlit 入口
├─ agent/                      # Agent 与工具
│  ├─ react_agent.py           # ReAct Agent 封装
│  └─ tools/
│     ├─ agent_tools.py        # RAG/天气/用户/报告数据等工具
│     └─ middleware.py         # 工具监控、动态提示词切换中间件
├─ rag/                        # RAG 服务
│  ├─ rag_service.py           # 检索 + 模型总结
│  └─ vector_store.py          # 文档切分、向量化、持久化
├─ model/
│  └─ factory.py               # 模型工厂（对话模型、Embedding）
├─ config/                     # YAML 配置
├─ prompts/                    # 提示词模板
├─ data/                       # 知识库文档与示例数据
│  └─ external/records.csv     # 演示用外部使用记录
└─ utils/                      # 配置/路径/日志/文件等工具
```

运行时生成的 `chroma_db/`（向量库）、`logs/`（日志）、`md5.text`（文件去重记录）不进入版本库。

## 快速开始

### 1. 安装依赖

```bash
pip install streamlit langchain langchain-community langchain-core \
  langchain-chroma langchain-text-splitters chromadb pypdf \
  pyyaml dashscope ollama nltk
```

### 2. 配置环境变量

模型密钥通过环境变量读取，请勿写入代码或配置文件：

```bash
export DASHSCOPE_API_KEY=你的通义千问/百炼 API Key
```

Windows PowerShell：

```powershell
$env:DASHSCOPE_API_KEY = "你的通义千问/百炼 API Key"
```

### 3. 加载知识库（首次运行）

将需要使用的知识文档放入 `data/`（支持 `.txt`、`.pdf`），然后执行：

```bash
python rag/vector_store.py
```

该命令会切分文档、生成向量并写入 Chroma；已处理过的文件会记录在 `md5.text`，避免重复入库。

### 4. 启动 Web 应用

```bash
streamlit run app.py
```

浏览器打开 Streamlit 提供的本地地址即可对话。

## 配置说明

配置文件位于 `config/`：

| 文件 | 作用 |
| --- | --- |
| `config/rag.yml` | 对话模型、Embedding 模型名称 |
| `config/chroma.yml` | 向量库目录、知识库目录、检索数量 `k`、切分参数等 |
| `config/prompts.yml` | 各类提示词模板文件路径 |
| `config/agent.yml` | Agent 外部数据文件路径 |

## Agent 工具

| 工具 | 说明 |
| --- | --- |
| `rag_summarize(query)` | 从向量库检索专业知识并总结 |
| `get_weather(city)` | 获取城市天气（当前为演示数据） |
| `get_user_location()` | 获取用户所在城市（当前为随机演示） |
| `get_user_id()` | 获取用户 ID（当前为随机演示） |
| `get_current_month()` | 获取当前月份（演示月份池） |
| `fetch_external_data(user_id, month)` | 查询用户某月使用记录（来自 `data/external/records.csv` 示例数据） |
| `fill_context_for_report()` | 触发报告生成场景的提示词切换 |

## 数据与隐私

- 仓库不包含任何 API Key、密钥等敏感信息，密钥统一通过环境变量注入。
- `data/external/records.csv` 为项目演示用的模拟使用记录，不包含真实用户个人数据。
- 生成文件（向量库、日志、MD5 记录、IDE 配置、Python 缓存等）已通过 `.gitignore` 排除。

