<p align="center">
  <a href="README.md">简体中文</a> · <b>English</b>
</p>

<h1 align="center">AI Customer Service System</h1>

<p align="center">
  <b>A RAG + Multi-Agent Conversation System for E-Commerce Customer Service</b><br>
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
  <a href="https://github.com/wang21225/AI-Smart-Customer-Service-Assistant"><img src="https://img.shields.io/github/stars/wang21225/AI-Smart-Customer-Service-Assistant?style=for-the-badge&logo=github&logoColor=white&label=GitHub" alt="GitHub Stars"></a>
  <a href="https://gitee.com/wmy221/faq-smart-ai-assistant"><img src="https://gitee.com/wmy221/faq-smart-ai-assistant/badge/star.svg?theme=dark" alt="Gitee Star"></a>
</p>

---

|  |  |
| :--- | :--- |
| **In one sentence** | User question → Intent recognition → Route to knowledge retrieval or business tools → Assemble context → Stream a sourced answer |
| **Try it instantly** | Runs out of the box — tables and demo data are created automatically; the full workflow works even without an LLM API key |

---

## 📖 Overview

A **decoupled front-end/back-end** intelligent customer service system. Customer-service conversations are modeled as a LangGraph directed state graph that chains intent recognition, knowledge retrieval, and business-tool invocation: answers are generated from RAG retrieval results with traceable sources, while orders can be queried and after-sales tickets created directly within a conversation. The front end offers three core capabilities: streaming chat, an operations dashboard, and knowledge-base management.

> On startup the system automatically creates tables and seeds demo data (products / FAQs / tickets). Even without an LLM API key configured, all local flows — database, conversations, knowledge base, tickets, and statistics — remain fully functional.

---

## ✨ Highlights

| Capability | Description |
| --- | --- |
| **Multi-agent workflow** | LangGraph directed state graph: intent recognition → routing → multi-turn tool calls → streaming generation, with state carried through the whole turn |
| **RAG knowledge Q&A** | Document loading (PDF / Word / Excel / Markdown) → chunking → embedding ingestion → BM25 + vector hybrid retrieval → source citations |
| **SSE streaming chat** | Typewriter-style token output, incremental parsing on the front end, Markdown rendering, and thumbs-up/down feedback |
| **End-to-end ticketing** | Query orders and create after-sales tickets in-conversation, with a seamless handoff to human agents |
| **Operations dashboard** | Real-time statistics on conversation trends, intent distribution, and top knowledge hits (ECharts) |
| **Zero-setup experience** | Automatic table creation and demo-data seeding on startup — no manual initialization |

---

## 🖼️ Screenshots

<div align="center">

| AI Chat | Operations Dashboard |
| :---: | :---: |
| <img src="docs/screenshots/chat.png" width="520"> | <img src="docs/screenshots/dashboard.png" width="520"> |

| Knowledge Base | RAG Retrieval Test |
| :---: | :---: |
| <img src="docs/screenshots/knowledge.png" width="520"> | <img src="docs/screenshots/retrieval.png" width="520"> |

| Support Tickets |
| :---: |
| <img src="docs/screenshots/tickets.png" width="520"> |

</div>

> Screenshots taken from a local demo environment (no LLM API key configured), showing the complete front-end/back-end interaction and data flow.

---

## 🏗️ Architecture

```mermaid
flowchart TD
    subgraph FE["Frontend Layer"]
        A["React 19 + Ant Design 5<br/>Streaming chat · Dashboard · Knowledge base · Tickets"]
    end

    subgraph API["API Layer"]
        B["FastAPI<br/>REST routes + SSE streaming responses"]
    end

    subgraph CORE["Agent Layer"]
        C["LangGraph service workflow<br/>Intent → Route → Tools → Generate"]
        D["RAG pipeline<br/>Load → Chunk → Embed → Hybrid retrieve"]
        E["Business tools<br/>Order query · Ticket creation"]
    end

    subgraph DATA["Data & Model Layer"]
        F["Chroma vector store"]
        G["MySQL 8.4<br/>Conversations / Tickets / Knowledge / Stats"]
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

The back end follows a layered architecture: `app/api` (routes) → `app/services` (business logic) → `app/repositories` (data access) → `app/models` (ORM models), alongside `app/core` (config / middleware / exceptions / responses), `app/rag` (RAG pipeline), `app/graphs` (LangGraph state machine), and `app/agents` (LLM wrappers).

Dependencies flow strictly top-down: the route layer never touches the database directly, and business logic stays unaware of HTTP details.

---

## 🔄 Conversation Flow

How a complete conversation turn is processed on the server:

```mermaid
sequenceDiagram
    autonumber
    participant U as User
    participant F as React Frontend
    participant A as FastAPI
    participant G as LangGraph
    participant R as RAG / Tools
    participant L as DashScope

    U->>F: Enter question
    F->>A: POST /api/chat/stream
    A->>G: Start service workflow
    G->>L: Intent recognition (qwen-turbo)
    L-->>G: Intent + confidence
    alt Knowledge question
        G->>R: BM25 + vector hybrid retrieval
        R-->>G: Matched chunks + sources
    else Business question
        G->>R: Call order / ticket tools
        R-->>G: Structured business result
    end
    G->>L: Generate answer (qwen-plus)
    L-->>G: Streamed tokens
    G-->>A: Chunk-by-chunk push
    A-->>F: SSE data events
    F-->>U: Typewriter rendering + source citations
```

---

## 🧩 Tech Stack

| Side | Technologies |
| :---: | :--- |
| Frontend | <img src="https://img.shields.io/badge/React_19-61DAFB?logo=react&logoColor=black"> <img src="https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white"> <img src="https://img.shields.io/badge/Vite_7-646CFF?logo=vite&logoColor=white"> <img src="https://img.shields.io/badge/Ant_Design_5-0170FE?logo=antdesign&logoColor=white"> <img src="https://img.shields.io/badge/Zustand-2D3748"> <img src="https://img.shields.io/badge/ECharts-AA344D?logo=apacheecharts&logoColor=white"> |
| Backend | <img src="https://img.shields.io/badge/Python_3.12-3776AB?logo=python&logoColor=white"> <img src="https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white"> <img src="https://img.shields.io/badge/Pydantic-E92063?logo=pydantic&logoColor=white"> <img src="https://img.shields.io/badge/SQLAlchemy_2-D71F00?logo=sqlalchemy&logoColor=white"> <img src="https://img.shields.io/badge/LangChain-1C3C3C?logo=langchain&logoColor=white"> <img src="https://img.shields.io/badge/LangGraph-1C3C3C"> |
| Data | <img src="https://img.shields.io/badge/MySQL_8.4-4479A1?logo=mysql&logoColor=white"> <img src="https://img.shields.io/badge/Chroma-FF6B6B"> <img src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white"> |
| Models | <img src="https://img.shields.io/badge/qwen--plus_chat-8B5CF6"> <img src="https://img.shields.io/badge/qwen--turbo_intent-8B5CF6"> <img src="https://img.shields.io/badge/text--embedding--v3-8B5CF6"> |

---

## 🚀 Quick Start

#### 1 · Start MySQL

```bash
docker compose up -d mysql
```

#### 2 · Start the backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate                      # Windows; use source .venv/bin/activate on macOS/Linux
pip install -r requirements.txt
copy .env.example .env                      # Windows; use cp .env.example .env on macOS/Linux
uvicorn app.main:app --reload --port 8000
```

On startup, tables are created automatically and demo data is seeded (four product categories, FAQs, and sample tickets) so you can try it immediately.

#### 3 · Start the frontend

```bash
cd frontend
npm install
npm run dev
```

#### 4 · Open

| Service | URL |
| --- | --- |
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| API docs (Swagger) | http://localhost:8000/docs |

---

## ⚙️ Configuration

The model API key is **injected only via `backend/.env`, never hard-coded**:

```env
DASHSCOPE_API_KEY=your-dashscope-api-key
CHAT_MODEL=qwen-plus               # Chat model
INTENT_MODEL=qwen-turbo            # Intent recognition model
EMBEDDING_MODEL=text-embedding-v3  # Embedding model
```

| Variable | Description | Default |
| --- | --- | --- |
| `DASHSCOPE_API_KEY` | DashScope (Bailian) API key — [apply here](https://bailian.console.aliyun.com/) | empty |
| `MYSQL_HOST / PORT / DATABASE / USERNAME / PASSWORD` | MySQL connection settings | localhost / 3306 / ai_customer_service / root / 123456 |
| `CHROMA_PERSIST_DIR` | Chroma vector-store persistence directory | ./data/chroma |
| `UPLOAD_DIR` | Knowledge document upload directory | ./data/uploads |
| `RAG_TOP_K` / `RAG_SCORE_THRESHOLD` | Retrieval count and relevance threshold | 5 / 0.35 |
| `INTENT_CONFIDENCE_THRESHOLD` | Intent-recognition confidence threshold | 0.55 |
| `BACKEND_CORS_ORIGINS` | Allowed frontend CORS origins | http://localhost:5173,http://127.0.0.1:5173 |

Without an API key, the system still runs normally: database, conversations, knowledge base, tickets, and statistics all work; LLM answers return a clear configuration hint instead.

---

## 🔌 Core API

| Method | Path | Description |
| --- | --- | --- |
| POST | `/api/chat/stream` | SSE streaming customer-service chat |
| POST | `/api/chat` | Non-streaming customer-service chat |
| GET/POST/DELETE | `/api/conversations` | Conversation management |
| GET/POST/PUT/DELETE | `/api/knowledge-bases` | Knowledge-base management |
| POST | `/api/knowledge-bases/{id}/documents` | Upload and vectorize knowledge documents |
| POST | `/api/retrieval/test` | Test knowledge retrieval online |
| GET/POST/PUT | `/api/tickets` | Ticket management |
| POST | `/api/feedback` | Conversation feedback |
| GET | `/api/dashboard/statistics` | Operations statistics |
| GET | `/health` | Health check |

---

## 🛠️ Engineering Highlights

- **LangGraph state-machine workflow**: conversations modeled as a directed state graph — intent recognition → routing → multi-turn tool calls → streaming generation, with state carried throughout
- **Standard RAG pipeline**: document loading (PDF/Word/Excel/Markdown) → text chunking → embedding ingestion → BM25 + vector hybrid retrieval → source citations
- **Deep front-end/back-end integration**: SSE stream parsing, conversation-scoped state management (Zustand), request-ID middleware, and a unified response schema
- **Production-minded details**: unified exception handling, structured logging, CORS configuration, auto-migration with demo data, one-click environment scripts, and smoke tests

---

## 📁 Project Structure

<details>
<summary>Click to expand</summary>

```
ai-chat/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/             # REST routes (chat / knowledge / tickets / dashboard ...)
│   │   ├── agents/          # LLM and intent-recognition wrappers
│   │   ├── core/            # Config, logging, middleware, unified exceptions & responses
│   │   ├── db/              # Database session and demo-data initialization
│   │   ├── graphs/          # LangGraph service workflow (state machine)
│   │   ├── models/          # SQLAlchemy ORM models
│   │   ├── rag/             # Document loading, chunking, embedding, retrieval
│   │   ├── repositories/    # Data access layer
│   │   ├── schemas/         # Pydantic request/response models
│   │   ├── services/        # Business logic layer
│   │   └── tools/           # Business tools callable by the agent
│   ├── scripts/             # DB initialization, smoke tests, etc.
│   ├── tests/               # Unit tests
│   ├── requirements.txt
│   └── .env.example         # Environment variable template
├── frontend/                # React frontend
│   └── src/
│       ├── pages/           # Chat / Dashboard / Knowledge / Retrieval / Tickets
│       ├── api/             # Axios request wrappers
│       ├── stores/          # Zustand state management
│       └── router/          # Frontend routing
├── docker-compose.yml       # MySQL dev environment
└── README.md
```

</details>

---

## ✅ Tests

```bash
cd backend
pytest tests/
```

---

<p align="center">
  <sub>MIT License · Mirrored on <a href="https://github.com/wang21225/AI-Smart-Customer-Service-Assistant">GitHub</a> & <a href="https://gitee.com/wmy221/faq-smart-ai-assistant">Gitee</a></sub>
</p>
