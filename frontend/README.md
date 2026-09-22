# 前端应用

React + TypeScript + Vite 打造的客服运营后台与聊天界面。

## 技术栈

React 19 · TypeScript · Vite 7 · Ant Design 5 · Zustand · ECharts · Axios · react-markdown

## 启动

```bash
npm install
npm run dev
```

默认访问 `http://localhost:5173`，通过 Vite 代理请求后端 `http://localhost:8000`。

## 页面

- **聊天页**（`/chat`）：SSE 流式对话、Markdown 渲染、对话反馈
- **数据看板**（`/`）：会话趋势、意图分布、知识命中 Top 统计
- **知识库**（`/knowledge`）：知识库与文档管理、上传向量化
- **检索测试**（`/retrieval`）：在线验证知识库检索效果
- **工单**（`/tickets`）：工单列表与处理