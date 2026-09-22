# 后端服务

FastAPI 后端，采用分层架构。

## 技术栈

Python 3.12 · FastAPI · SQLAlchemy 2 · LangGraph · LangChain · Chroma · SSE

## 启动

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8000
```

应用启动时自动建表并写入演示数据。也可以手动执行：

```bash
python scripts/init_db.py
```

## 目录结构

```
app/
├── api/           # REST 路由（chat / knowledge / tickets / dashboard / feedback ...）
├── agents/        # 大模型封装与意图识别
├── core/          # 配置、日志、中间件、统一异常与响应
├── db/            # 数据库会话与演示数据初始化
├── graphs/        # LangGraph 客服工作流（状态机）
├── models/        # SQLAlchemy ORM 模型
├── rag/           # 文档加载、切分、向量化与检索
├── repositories/  # 数据访问层
├── schemas/       # Pydantic 请求/响应模型
├── services/      # 业务逻辑层
└── tools/         # 客服可调用业务工具
```

## 核心接口

- `POST /api/chat/stream`：SSE 流式客服对话
- `POST /api/chat`：非流式客服对话
- `GET/POST/DELETE /api/conversations`：会话管理
- `GET/POST/PUT/DELETE /api/knowledge-bases`：知识库管理
- `POST /api/knowledge-bases/{id}/documents`：上传并向量化知识文档
- `POST /api/retrieval/test`：在线测试知识库检索
- `GET /api/dashboard/statistics`：运营数据统计

接口文档见 http://localhost:8000/docs （Swagger UI）。

## 测试

```bash
pytest tests/
```

## 说明

业务数据写入 MySQL，向量索引写入 Chroma。API Key 不写入代码，只从 `.env` 读取。