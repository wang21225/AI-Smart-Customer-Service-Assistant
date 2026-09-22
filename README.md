<p align="center">
  <span style="font-size: 42px; font-weight: 800; letter-spacing: 1px; background: linear-gradient(135deg, #6366f1, #8b5cf6); -webkit-background-clip: text; background-clip: text; color: transparent;">AI 智能客服系统</span>
</p>

<p align="center">
  <span style="color: #6b7280; font-size: 16px;">前后端分离 · 多智能体工作流 · RAG 知识库 · SSE 流式对话</span>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
  <a href="https://gitee.com/wmy221/faq-smart-ai-assistant"><img src="https://gitee.com/wmy221/faq-smart-ai-assistant/badge/star.svg" alt="Star"></a>
  <a href="https://gitee.com/wmy221/faq-smart-ai-assistant"><img src="https://gitee.com/wmy221/faq-smart-ai-assistant/badge/fork.svg" alt="Fork"></a>
</p>

<p align="center" style="color: #9ca3af; font-size: 14px;">
  基于阿里云百炼（DashScope）大模型构建：React + Ant Design 前端 · FastAPI 后端 · MySQL + Chroma 数据层
</p>

---

## 功能亮点

<div align="center">

| | | |
| :---: | :---: | :---: |
| <div style="width:240px;height:110px;padding:20px;border-radius:14px;border:1px solid #e5e7eb;background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.06);text-align:left"><b>多智能体工作流</b><br><span style="color:#6b7280;font-size:13px;line-height:1.7">LangGraph 有向状态图：意图识别 → 路由 → 多轮工具调用 → 流式生成</span></div> | <div style="width:240px;height:110px;padding:20px;border-radius:14px;border:1px solid #e5e7eb;background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.06);text-align:left"><b>RAG 知识库问答</b><br><span style="color:#6b7280;font-size:13px;line-height:1.7">文档切分 → Embedding 入库 → 混合检索，回答附带可追溯的知识来源</span></div> | <div style="width:240px;height:110px;padding:20px;border-radius:14px;border:1px solid #e5e7eb;background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.06);text-align:left"><b>SSE 流式对话</b><br><span style="color:#6b7280;font-size:13px;line-height:1.7">打字机式流式回复，支持 Markdown 渲染与对话点赞 / 点踩反馈</span></div> |
| <div style="width:240px;height:110px;padding:20px;border-radius:14px;border:1px solid #e5e7eb;background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.06);text-align:left"><b>业务工单闭环</b><br><span style="color:#6b7280;font-size:13px;line-height:1.7">会话中直接查询订单，一键创建售后工单，转人工无缝衔接</span></div> | <div style="width:240px;height:110px;padding:20px;border-radius:14px;border:1px solid #e5e7eb;background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.06);text-align:left"><b>运营数据看板</b><br><span style="color:#6b7280;font-size:13px;line-height:1.7">会话趋势、意图分布、知识命中 Top 实时统计（ECharts）</span></div> | <div style="width:240px;height:110px;padding:20px;border-radius:14px;border:1px solid #e5e7eb;background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.06);text-align:left"><b>一键开箱体验</b><br><span style="color:#6b7280;font-size:13px;line-height:1.7">启动自动建表并写入演示数据（商品 / FAQ / 工单），无需手动初始化</span></div> |

</div>

---

## 界面预览

<div align="center">

| 智能客服对话 | 运营数据看板 |
| :---: | :---: |
| <img src="docs/screenshots/chat.png" width="540"> | <img src="docs/screenshots/dashboard.png" width="540"> |

| 知识库管理 | RAG 检索测试 |
| :---: | :---: |
| <img src="docs/screenshots/knowledge.png" width="540"> | <img src="docs/screenshots/retrieval.png" width="540"> |

| 客服工单 |
| :---: |
| <img src="docs/screenshots/tickets.png" width="540"> |

</div>

> 截图来自本地演示环境（未配置大模型 API Key），展示完整的前后端交互与数据闭环。

---

## 技术栈

<div align="center">

| 端 | 技术 |
| :---: | :--- |
| 前端 | <span style="display:inline-block;padding:2px 10px;margin:2px;border-radius:999px;background:#eef2ff;color:#3730a3;font-size:13px;">React 19</span><span style="display:inline-block;padding:2px 10px;margin:2px;border-radius:999px;background:#eef2ff;color:#3730a3;font-size:13px;">TypeScript</span><span style="display:inline-block;padding:2px 10px;margin:2px;border-radius:999px;background:#eef2ff;color:#3730a3;font-size:13px;">Vite 7</span><span style="display:inline-block;padding:2px 10px;margin:2px;border-radius:999px;background:#eef2ff;color:#3730a3;font-size:13px;">Ant Design 5</span><span style="display:inline-block;padding:2px 10px;margin:2px;border-radius:999px;background:#eef2ff;color:#3730a3;font-size:13px;">Zustand</span><span style="display:inline-block;padding:2px 10px;margin:2px;border-radius:999px;background:#eef2ff;color:#3730a3;font-size:13px;">ECharts</span> |
| 后端 | <span style="display:inline-block;padding:2px 10px;margin:2px;border-radius:999px;background:#f5f3ff;color:#5b21b6;font-size:13px;">Python 3.12</span><span style="display:inline-block;padding:2px 10px;margin:2px;border-radius:999px;background:#f5f3ff;color:#5b21b6;font-size:13px;">FastAPI</span><span style="display:inline-block;padding:2px 10px;margin:2px;border-radius:999px;background:#f5f3ff;color:#5b21b6;font-size:13px;">SQLAlchemy 2</span><span style="display:inline-block;padding:2px 10px;margin:2px;border-radius:999px;background:#f5f3ff;color:#5b21b6;font-size:13px;">LangGraph</span><span style="display:inline-block;padding:2px 10px;margin:2px;border-radius:999px;background:#f5f3ff;color:#5b21b6;font-size:13px;">LangChain</span><span style="display:inline-block;padding:2px 10px;margin:2px;border-radius:999px;background:#f5f3ff;color:#5b21b6;font-size:13px;">Chroma</span> |
| 数据 | <span style="display:inline-block;padding:2px 10px;margin:2px;border-radius:999px;background:#ecfdf5;color:#065f46;font-size:13px;">MySQL 8.4</span><span style="display:inline-block;padding:2px 10px;margin:2px;border-radius:999px;background:#ecfdf5;color:#065f46;font-size:13px;">Chroma 向量库</span><span style="display:inline-block;padding:2px 10px;margin:2px;border-radius:999px;background:#ecfdf5;color:#065f46;font-size:13px;">文件存储</span> |
| 模型 | <span style="display:inline-block;padding:2px 10px;margin:2px;border-radius:999px;background:#fff7ed;color:#9a3412;font-size:13px;">qwen-plus 对话</span><span style="display:inline-block;padding:2px 10px;margin:2px;border-radius:999px;background:#fff7ed;color:#9a3412;font-size:13px;">qwen-turbo 意图</span><span style="display:inline-block;padding:2px 10px;margin:2px;border-radius:999px;background:#fff7ed;color:#9a3412;font-size:13px;">text-embedding-v3 向量</span> |

</div>

---

## 核心架构

<div align="center">

<span style="display:inline-block;padding:12px 28px;border-radius:12px;border:1px solid #e5e7eb;background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.06);font-weight:600;">React 前端 <span style="color:#9ca3af;font-weight:400;">管理后台 + 聊天界面</span></span>

<span style="color:#a5b4fc;font-size:18px;">▼</span><br/>
<span style="color:#9ca3af;font-size:12px;">HTTP / SSE</span>

<span style="display:inline-block;padding:12px 28px;border-radius:12px;border:1px solid #e5e7eb;background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.06);font-weight:600;">FastAPI <span style="color:#9ca3af;font-weight:400;">路由层：REST + 流式</span></span>

<span style="color:#a5b4fc;font-size:18px;">▼</span><br/>
<span style="color:#9ca3af;font-size:12px;">状态流转</span>

<span style="display:inline-block;padding:12px 28px;border-radius:12px;border:1px solid #c7d2fe;background:#eef2ff;box-shadow:0 1px 3px rgba(0,0,0,.06);font-weight:700;color:#3730a3;">LangGraph 客服工作流</span>

<span style="color:#a5b4fc;font-size:18px;">▼</span><br/>
<span style="color:#9ca3af;font-size:12px;">结果分流</span>

<table><tr>
<td width="50%" align="center"><span style="display:inline-block;padding:12px 20px;border-radius:12px;border:1px solid #e5e7eb;background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.06);"><b>RAG 流水线</b><br><span style="color:#6b7280;font-size:12px;">加载 → 切分 → Embedding → Chroma 检索</span></span></td>
<td width="50%" align="center"><span style="display:inline-block;padding:12px 20px;border-radius:12px;border:1px solid #e5e7eb;background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.06);"><b>业务工具</b><br><span style="color:#6b7280;font-size:12px;">订单查询 · 工单创建</span></span></td>
</tr></table>

<span style="color:#a5b4fc;font-size:18px;">▼</span>

<table><tr>
<td width="50%" align="center"><span style="display:inline-block;padding:12px 20px;border-radius:12px;border:1px solid #fde68a;background:#fffbeb;box-shadow:0 1px 3px rgba(0,0,0,.06);font-weight:600;">DashScope 大模型<br><span style="color:#9a3412;font-size:12px;font-weight:400;">LLM / Embedding</span></span></td>
<td width="50%" align="center"><span style="display:inline-block;padding:12px 20px;border-radius:12px;border:1px solid #a7f3d0;background:#ecfdf5;box-shadow:0 1px 3px rgba(0,0,0,.06);font-weight:600;">MySQL + 文件存储<br><span style="color:#065f46;font-size:12px;font-weight:400;">会话 / 工单 / 知识库 / 统计</span></span></td>
</tr></table>

</div>

后端采用分层架构：`app/api`（路由）→ `app/services`（业务）→ `app/repositories`（数据访问）→ `app/models`（ORM 模型），另含 `app/core`（配置 / 中间件 / 异常 / 响应）、`app/rag`（RAG 流水线）、`app/graphs`（LangGraph 状态机）、`app/agents`（大模型封装）。

---

## 项目结构

<details>
<summary>查看目录结构</summary>

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

## 快速开始

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

## 配置说明

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

## 核心 API

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

## 工程亮点

- **LangGraph 状态机工作流**：客服对话被建模为有向状态图，意图识别 → 路由 → 多轮工具调用 → 流式生成，状态贯穿全程
- **标准 RAG 流水线**：文档加载（PDF/Word/Excel/Markdown）→ 文本切分 → Embedding 入库 → BM25 + 向量混合检索 → 来源引用
- **前后端深度集成**：SSE 流式解析、会话级状态管理（Zustand）、请求 ID 中间件与统一响应体
- **工程化细节**：统一异常处理、结构化日志、CORS 配置、自动建表与演示数据、一键环境脚本、冒烟测试

---

## 测试

```bash
cd backend
pytest tests/
```

---

<p align="center" style="color:#9ca3af; font-size: 13px;">
  MIT License · 由 <a href="https://gitee.com/wmy221/faq-smart-ai-assistant">Gitee</a> 托管
</p>