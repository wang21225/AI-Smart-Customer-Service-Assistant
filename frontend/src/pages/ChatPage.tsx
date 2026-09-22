import { CopyOutlined, DeleteOutlined, LikeOutlined, PlusOutlined, SendOutlined, StopOutlined } from "@ant-design/icons";
import { Avatar, Button, Empty, Input, List, Popconfirm, Space, Tag, Tooltip, Typography, message } from "antd";
import { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";

import { useChatStore } from "../stores/chatStore";

export function ChatPage() {
  const [input, setInput] = useState("");
  const bottomRef = useRef<HTMLDivElement>(null);
  const {
    conversations,
    messages,
    activeSessionId,
    intent,
    sources,
    statusText,
    loading,
    loadConversations,
    openConversation,
    deleteConversation,
    newConversation,
    sendMessage
  } = useChatStore();

  useEffect(() => {
    loadConversations();
  }, [loadConversations]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const submit = async () => {
    if (!input.trim()) return;
    const value = input.trim();
    setInput("");
    await sendMessage(value);
  };

  return (
    <div className="chat-grid">
      <aside className="panel session-panel">
        <Button type="primary" icon={<PlusOutlined />} block onClick={newConversation}>
          新建会话
        </Button>
        <List
          dataSource={conversations}
          locale={{ emptyText: <Empty description="暂无历史会话" /> }}
          renderItem={(item) => (
            <List.Item
              className={item.id === activeSessionId ? "session-item active" : "session-item"}
              onClick={() => openConversation(item.id)}
              actions={[
                <Popconfirm key="delete" title="删除会话" description="确定删除这个历史会话吗？" onConfirm={() => deleteConversation(item.id)}>
                  <Button
                    className="session-delete-button"
                    type="text"
                    size="small"
                    icon={<DeleteOutlined />}
                    onClick={(event) => event.stopPropagation()}
                  />
                </Popconfirm>
              ]}
            >
              <List.Item.Meta title={item.title} description={item.last_intent || "等待提问"} />
            </List.Item>
          )}
        />
      </aside>

      <main className="panel chat-panel">
        <div className="chat-header">
          <Space>
            <Avatar className="ai-avatar">AI</Avatar>
            <div>
              <Typography.Title level={4}>企业 AI 客服</Typography.Title>
              <Typography.Text type="secondary">在线 · qwen-plus · 默认知识库</Typography.Text>
            </div>
          </Space>
          <Space>
            <Button icon={<StopOutlined />} disabled={!loading}>
              停止
            </Button>
            <Button danger onClick={newConversation}>
              清空
            </Button>
          </Space>
        </div>

        <div className="message-list">
          {messages.length === 0 && (
            <div className="welcome">
              <Typography.Title>你好，我是 AI 智能客服</Typography.Title>
              <Typography.Text>可以试试：“帮我查询订单 202607160001 到哪里了”</Typography.Text>
              <Space wrap>
                {["退款政策是什么？", "商品签收后几天可以退货？", "我要投诉，转人工"].map((item) => (
                  <Button key={item} onClick={() => setInput(item)}>
                    {item}
                  </Button>
                ))}
              </Space>
            </div>
          )}
          {messages.map((item, index) => (
            <div key={index} className={`message ${item.role}`}>
              <Avatar>{item.role === "user" ? "我" : "AI"}</Avatar>
              <div className="bubble">
                <ReactMarkdown>{item.content}</ReactMarkdown>
                <div className="message-actions">
                  <Tooltip title="复制">
                    <Button
                      className="message-action-button"
                      type="text"
                      size="small"
                      icon={<CopyOutlined />}
                      onClick={() => navigator.clipboard.writeText(item.content)}
                    />
                  </Tooltip>
                  {item.role === "assistant" && (
                    <Tooltip title="有帮助">
                      <Button
                        className="message-action-button"
                        type="text"
                        size="small"
                        icon={<LikeOutlined />}
                        onClick={() => message.success("感谢反馈")}
                      />
                    </Tooltip>
                  )}
                </div>
              </div>
            </div>
          ))}
          {loading && <div className="status-line">{statusText}</div>}
          <div ref={bottomRef} />
        </div>

        <div className="composer">
          <div className="composer-box">
            <Input.TextArea
              className="composer-input"
              value={input}
              onChange={(event) => setInput(event.target.value)}
              autoSize={{ minRows: 2, maxRows: 6 }}
              placeholder="输入你的问题，例如：商品签收后几天可以退货？"
              onPressEnter={(event) => {
                if (!event.shiftKey) {
                  event.preventDefault();
                  submit();
                }
              }}
            />
            <div className="composer-footer">
              <span>Enter 发送 · Shift + Enter 换行</span>
              <Tooltip title="发送">
                <Button
                  className="composer-send"
                  type="primary"
                  icon={<SendOutlined />}
                  loading={loading}
                  disabled={!input.trim()}
                  onClick={submit}
                />
              </Tooltip>
            </div>
          </div>
        </div>
      </main>

      <aside className="panel insight-panel">
        <Typography.Title level={5}>处理状态</Typography.Title>
        <Tag color="blue">{intent || "等待识别"}</Tag>
        <Typography.Title level={5}>知识引用</Typography.Title>
        {sources.length === 0 ? (
          <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} description="暂无引用" />
        ) : (
          sources.map((source) => (
            <div className="source-card" key={`${source.document_name}-${source.page_no}-${source.score}`}>
              <Typography.Text strong>{source.document_name}</Typography.Text>
              <Typography.Text type="secondary">第 {source.page_no} 页 · 相关度 {source.score}</Typography.Text>
              <p>{source.snippet}</p>
            </div>
          ))
        )}
      </aside>
    </div>
  );
}
