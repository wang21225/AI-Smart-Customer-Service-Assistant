<h1 align="center">AI 智能客服系统</h1>

<p align="center">
  <b>面向电商客服场景的 RAG + 多智能体对话系统</b><br>
  <sub>React 19 · FastAPI · LangGraph · Chroma · MySQL 8.4 · DashScope</sub>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-6366f1?style=for-the-badge" alt="License"></a>
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black" alt="React">
  <img src="https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/MySQL-8.4-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL">
  <img src="https://img.shields.io/badge/DashScope-qwen-8B5CF6?style=for-the-badge" alt="DashScope">
</p>

<p align="center">
  <a href="https://gitee.com/wmy221/faq-smart-ai-assistant"><img src="https://gitee.com/wmy221/faq-smart-ai-assistant/badge/star.svg?theme=dark" alt="Gitee Star"></a>
  <a href="https://gitee.com/wmy221/faq-smart-ai-assistant"><img src="https://gitee.com/wmy221/faq-smart-ai-assistant/badge/fork.svg?theme=dark" alt="Gitee Fork"></a>
</p>

---

|  |  |
| :--- | :--- |
| **一句话概括** | 用户提问 → 意图识别 → 分流到知识检索或业务工具 → 拼装上下文 → 流式生成带来源的回答 |
| **在线体验** | 启动即用，自动建表并写入演示数据，无需配置大模型 Key 也可跑通全流程 |

---

## 📖 项目简介

一个**前后端分离**的智能客服系统。项目把客服对话建模为 LangGraph 有向状态图，串联起意图识别、知识检索与业务工具调用：回答基于 RAG 检索结果生成并附带可追溯来源，同时支持在会话中直接查询订单、创建售后工单。前端提供流式对话、运营看板与知识库管理三块能力。

> 系统启动时自动建表并写入演示数据（商品 / FAQ / 工单），即使未配置大模型 API Key，数据库、会话、知识库、工单与统计等本地流程也完整可用。

---

## ✨ 功能亮点

| 能力 | 说明 |
| --- | --- |
| **多智能体工作流** | LangGraph 有向状态图：意图识别 → 路由 → 多轮工具调用 → 流式生成，状态贯穿整轮对话 |
| **RAG 知识库问答** | 文档加载（PDF / Word / Excel / Markdown）→ 切分 → Embedding 入库 → BM25 + 向量混合检索 → 来源引用 |
| **SSE 流式对话** | 打字机式逐段输出，前端增量解析，支持 Markdown 渲染与点赞 / 点踩反馈 |
| **业务工单闭环** | 会话中直接查询订单、一键创建售后工单，转人工无缝衔接 |
| **运营数据看板** | 会话趋势、意图分布、知识命中 Top 榜实时统计（ECharts） |
| **一键开箱体验** | 启动自动建表并写入演示数据，无需手动初始化 |

---

## 🖼️ 界面预览

<div align="center">

| 智能客服对话 | 运营数据看板 |
| :---: | :---: |
| <img src="docs/screenshots/chat.png" width="520"> | <img src="docs/screenshots/dashboard.png" width="520"> |

| 知识库管理 | RAG 检索测试 |
| :---: | :---: |
| <img src="docs/screenshots/knowledge.png" width="520"> | <img src="docs/screenshots/retrieval.png" width="520"> |

| 客服工单 |
| :---: |
| <img src="docs/screenshots/tickets.png" width="520"> |

</div>

> 截图来自本地演示环境（未配置大模型 API Key），展示完整的前后端交互与数据闭环。

---

## 🏗️ 核心架构

```mermaid
flowchart TD
    subgraph FE["前端层"]
        A["React 19 + Ant Design 5<br/>流式对话 · 运营看板 · 知识库管理 · 工单"]
    end

    subgraph API["接口层"]
        B["FastAPI<br/>REST 路由 + SSE 流式响应"]
    end

    subgraph CORE["智能体层"]
        C["LangGraph 客服工作流<br/>意图识别 → 路由 → 工具调用 → 生成"]
        D["RAG 流水线<br/>加载 → 切分 → 向量化 → 混合检索"]
        E["业务工具<br/>订单查询 · 工单创建"]
    end

    subgraph DATA["数据与模型层"]
        F["Chroma 向量库"]
        G["MySQL 8.4<br/>会话 / 工单 / 知识库 / 统计"]
        H["DashScope<br/>qwen-plus · text-embedding-v3"]
    end

    A -->|"HTTP / SSE"| B
    B --> C
    C --> D
    C --> E
    C --> H
    D --> F
    D --> H
    E --> G
    B --> G
```

后端采用分层架构：`app/api`（路由）→ `app/services`（业务）→ `app/repositories`（数据访问）→ `app/models`（ORM 模型），另含 `app/core`（配置 / 中间件 / 异常 / 响应）、`app/rag`（RAG 流水线）、`app/graphs`（LangGraph 状态机）、`app/agents`（大模型封装）。

依赖方向自上而下单向流动，路由层不直接触碰数据库，业务逻辑不感知 HTTP 细节。

---

## 🔄 对话时序

一轮完整对话在服务端的流转过程：

```mermaid
sequenceDiagram
    autonumber
    participant U as 用户
    participant F as React 前端
    participant A as FastAPI
    participant G as LangGraph
    participant R as RAG / 工具
    participant L as DashScope

    U->>F: 输入问题
    F->>A: POST /api/chat/stream
    A->>G: 启动客服工作流
    G->>L: 意图识别（qwen-turbo）
    L-->>G: 意图 + 置信度
    alt 知识类问题
        G->>R: BM25 + 向量混合检索
        R-->>G: 命中片段 + 来源
    else 业务类问题
        G->>R: 调用订单 / 工单工具
        R-->>G: 结构化业务结果
    end
    G->>L: 生成回答（qwen-plus）
    L-->>G: 流式 token
    G-->>A: 逐段推送
    A-->>F: SSE data 事件
    F-->>U: 打字机式渲染 + 来源引用
```

---

## 🧩 技术选型

| 端 | 技术 |
| :---: | :--- |
| 前端 | <img src="https://img.shields.io/badge/React_19-61DAFB?logo=react&logoColor=black"> <img src="https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white"> <img src="https://img.shields.io/badge/Vite_7-646CFF?logo=vite&logoColor=white"> <img src="https://img.shields.io/badge/Ant_Design_5-0170FE?logo=antdesign&logoColor=white"> <img src="https://img.shields.io/badge/Zustand-2D3748"> <img src="https://img.shields.io/badge/ECharts-AA344D?logo=apacheecharts&logoColor=white"> |
| 后端 | <img src="https://img.shields.io/badge/Python_3.12-3776AB?logo=python&logoColor=white"> <img src="https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white"> <img src="https://img.shields.io/badge/Pydantic-E92063?logo=pydantic&logoColor=white"> <img src="https://img.shields.io/badge/SQLAlchemy_2-D71F00?logo=sqlalchemy&logoColor=white"> <img src="https://img.shields.io/badge/LangChain-1C3C3C?logo=langchain&logoColor=white"> <img src="https://img.shields.io/badge/LangGraph-1C3C3C"> |
| 数据 | <img src="https://img.shields.io/badge/MySQL_8.4-4479A1?logo=mysql&logoColor=white"> <img src="https://img.shields.io/badge/Chroma-FF6B6B"> <img src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white"> |
| 模型 | <img src="https://img.shields.io/badge/qwen--plus_对话-8B5CF6"> <img src="https://img.shields.io/badge/qwen--turbo_意图-8B5CF6"> <img src="https://img.shields.io/badge/text--embedding--v3_向量-8B5CF6"> |

---

## 🚀 快速开始

#### 1 · 启动 MySQL

```bash
docker compose up -d mysql
```

#### 2 · 启动后端

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate                      # Windows；macOS/Linux 请使用 source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env                      # Windows；macOS/Linux 请使用 cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

应用启动时会自动建表并写入演示数据（四类商品、FAQ、示例工单），便于直接体验。

#### 3 · 启动前端

```bash
cd frontend
npm install
npm run dev
```

#### 4 · 访问

| 服务 | 地址 |
| --- | --- |
| 前端应用 | http://localhost:5173 |
| 后端接口 | http://localhost:8000 |
| API 文档（Swagger） | http://localhost:8000/docs |

---

## ⚙️ 配置说明

模型 API Key **只通过 `backend/.env` 注入，不写入代码**：

```env
DASHSCOPE_API_KEY=请填写你的百炼 API Key
CHAT_MODEL=qwen-plus            # 对话模型
INTENT_MODEL=qwen-turbo         # 意图识别模型
EMBEDDING_MODEL=text-embedding-v3  # 向量模型
```

| 变量 | 说明 | 默认值 |
| --- | --- | --- |
| `DASHSCOPE_API_KEY` | 百炼平台 API Key，[申请地址](https://bailian.console.aliyun.com/) | 空 |
| `MYSQL_HOST / PORT / DATABASE / USERNAME / PASSWORD` | MySQL 连接配置 | localhost / 3306 / ai_customer_service / root / 123456 |
| `CHROMA_PERSIST_DIR` | Chroma 向量库持久化目录 | ./data/chroma |
| `UPLOAD_DIR` | 知识库文档上传目录 | ./data/uploads |
| `RAG_TOP_K` / `RAG_SCORE_THRESHOLD` | 检索数量与相关性阈值 | 5 / 0.35 |
| `INTENT_CONFIDENCE_THRESHOLD` | 意图识别置信度阈值 | 0.55 |
| `BACKEND_CORS_ORIGINS` | 允许的前端跨域来源 | http://localhost:5173,http://127.0.0.1:5173 |

未配置 API Key 时，系统仍可正常运行：数据库、会话、知识库、工单、统计等本地流程完整可用，大模型回答会返回明确的配置提示。

---

## 🔌 核心 API

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/api/chat/stream` | SSE 流式客服对话 |
| POST | `/api/chat` | 非流式客服对话 |
| GET/POST/DELETE | `/api/conversations` | 会话管理 |
| GET/POST/PUT/DELETE | `/api/knowledge-bases` | 知识库管理 |
| POST | `/api/knowledge-bases/{id}/documents` | 上传并向量化知识文档 |
| POST | `/api/retrieval/test` | 在线测试知识库检索 |
| GET/POST/PUT | `/api/tickets` | 工单管理 |
| POST | `/api/feedback` | 对话反馈 |
| GET | `/api/dashboard/statistics` | 运营数据统计 |
| GET | `/health` | 健康检查 |

---

## 🛠️ 工程亮点

- **LangGraph 状态机工作流**：客服对话被建模为有向状态图，意图识别 → 路由 → 多轮工具调用 → 流式生成，状态贯穿全程
- **标准 RAG 流水线**：文档加载（PDF/Word/Excel/Markdown）→ 文本切分 → Embedding 入库 → BM25 + 向量混合检索 → 来源引用
- **前后端深度集成**：SSE 流式解析、会话级状态管理（Zustand）、请求 ID 中间件与统一响应体
- **工程化细节**：统一异常处理、结构化日志、CORS 配置、自动建表与演示数据、一键环境脚本、冒烟测试

---

## 📁 项目结构

<details>
<summary>展开目录结构</summary>

```
ai-chat/
├── backend/                 # FastAPI 后端
│   ├── app/
│   │   ├── api/             # REST 路由（chat / knowledge / tickets / dashboard ...）
│   │   ├── agents/          # 大模型与意图识别封装
│   │   ├── core/            # 配置、日志、中间件、统一异常与响应
│   │   ├── db/              # 数据库会话与演示数据初始化
│   │   ├── graphs/          # LangGraph 客服工作流（状态机）
│   │   ├── models/          # SQLAlchemy ORM 模型
│   │   ├── rag/             # 文档加载、切分、向量化与检索
│   │   ├── repositories/    # 数据访问层
│   │   ├── schemas/         # Pydantic 请求/响应模型
│   │   ├── services/        # 业务逻辑层
│   │   └── tools/           # 客服可调用的业务工具
│   ├── scripts/             # 数据库初始化、冒烟测试等脚本
│   ├── tests/               # 单元测试
│   ├── requirements.txt
│   └── .env.example         # 环境变量模板
├── frontend/                # React 前端
│   └── src/
│       ├── pages/           # 聊天 / 看板 / 知识库 / 检索 / 工单页面
│       ├── api/             # Axios 请求封装
│       ├── stores/          # Zustand 状态管理
│       └── router/          # 前端路由
├── docker-compose.yml       # MySQL 开发环境
└── README.md
```

</details>

---

## ✅ 测试

```bash
cd backend
pytest tests/
```

---

<p align="center">
  <sub>MIT License · 由 <a href="https://gitee.com/wmy221/faq-smart-ai-assistant">Gitee</a> 托管</sub>
</p>