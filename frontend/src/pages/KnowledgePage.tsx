import { DeleteOutlined, EyeOutlined, UploadOutlined } from "@ant-design/icons";
import { Button, Card, Drawer, Empty, Form, Input, List, Modal, Popconfirm, Space, Table, Tag, Typography, Upload, message } from "antd";
import { useEffect, useState } from "react";

import { apiDelete, apiGet, apiPost } from "../api/client";
import type { DocumentChunk, KnowledgeBase, KnowledgeDocument } from "../types";

export function KnowledgePage() {
  const [items, setItems] = useState<KnowledgeBase[]>([]);
  const [active, setActive] = useState<KnowledgeBase>();
  const [docs, setDocs] = useState<KnowledgeDocument[]>([]);
  const [chunks, setChunks] = useState<DocumentChunk[]>([]);
  const [chunkDoc, setChunkDoc] = useState<KnowledgeDocument>();
  const [open, setOpen] = useState(false);
  const [chunkOpen, setChunkOpen] = useState(false);
  const [form] = Form.useForm();

  const load = async () => {
    const data = await apiGet<KnowledgeBase[]>("/knowledge-bases");
    setItems(data);
    if (!active && data[0]) setActive(data[0]);
  };

  const loadDocuments = async (knowledgeBaseId: number) => {
    setDocs(await apiGet<KnowledgeDocument[]>(`/knowledge-bases/${knowledgeBaseId}/documents`));
  };

  const showChunks = async (document: KnowledgeDocument) => {
    setChunkDoc(document);
    setChunks(await apiGet<DocumentChunk[]>(`/documents/${document.id}/chunks`));
    setChunkOpen(true);
  };

  const deleteDocument = async (document: KnowledgeDocument) => {
    await apiDelete(`/documents/${document.id}`);
    message.success("文件已删除");
    if (active) await loadDocuments(active.id);
    if (chunkDoc?.id === document.id) {
      setChunkOpen(false);
      setChunks([]);
      setChunkDoc(undefined);
    }
  };

  const deleteChunk = async (chunk: DocumentChunk) => {
    await apiDelete(`/chunks/${chunk.id}`);
    message.success("分片已删除");
    const nextChunks = chunks.filter((item) => item.id !== chunk.id);
    setChunks(nextChunks);
    if (active) await loadDocuments(active.id);
  };

  const clearChunks = async () => {
    if (!chunkDoc) return;
    await apiDelete(`/documents/${chunkDoc.id}/chunks`);
    message.success("分片已清空");
    setChunks([]);
    if (active) await loadDocuments(active.id);
  };

  const deleteKnowledgeBase = async (item: KnowledgeBase) => {
    await apiDelete(`/knowledge-bases/${item.id}`);
    message.success("知识库已删除");
    const nextItems = await apiGet<KnowledgeBase[]>("/knowledge-bases");
    setItems(nextItems);
    if (active?.id === item.id) {
      setActive(nextItems[0]);
      setDocs([]);
      setChunks([]);
      setChunkDoc(undefined);
      setChunkOpen(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  useEffect(() => {
    if (active) loadDocuments(active.id);
  }, [active]);

  return (
    <div className="knowledge-grid">
      <Card className="knowledge-side-card" title="知识库" extra={<Button type="primary" onClick={() => setOpen(true)}>创建知识库</Button>}>
        <List<KnowledgeBase>
          dataSource={items}
          locale={{ emptyText: <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} description="暂无知识库" /> }}
          renderItem={(item) => (
            <List.Item
              className={active?.id === item.id ? "kb-active" : ""}
              onClick={() => setActive(item)}
              actions={[
                <Popconfirm
                  key="delete"
                  title="删除知识库"
                  description="将同时删除该知识库下的文件和分片，确定删除吗？"
                  onConfirm={() => deleteKnowledgeBase(item)}
                >
                  <Button
                    size="small"
                    danger
                    type="text"
                    icon={<DeleteOutlined />}
                    onClick={(event) => event.stopPropagation()}
                  />
                </Popconfirm>
              ]}
            >
              <List.Item.Meta title={item.name} description={item.description || "暂无描述"} />
            </List.Item>
          )}
        />
      </Card>

      <Card
        className="knowledge-document-card"
        title={
          <div className="document-card-title">
            <Typography.Text strong>{active ? `${active.name} · 文档` : "请选择知识库"}</Typography.Text>
            <Typography.Text type="secondary">{active ? `${docs.length} 个文件` : "选择左侧知识库后查看文档"}</Typography.Text>
          </div>
        }
        extra={
          <Upload
            showUploadList={false}
            customRequest={async ({ file, onSuccess, onError }) => {
              if (!active) return;
              const formData = new FormData();
              formData.append("file", file as File);
              try {
                await fetch(`/api/knowledge-bases/${active.id}/documents`, { method: "POST", body: formData });
                message.success("上传并处理完成");
                await loadDocuments(active.id);
                onSuccess?.({});
              } catch (error) {
                onError?.(error as Error);
              }
            }}
          >
            <Button icon={<UploadOutlined />} disabled={!active}>上传文件</Button>
          </Upload>
        }
      >
        <Table<KnowledgeDocument>
          rowKey="id"
          size="middle"
          dataSource={docs}
          pagination={false}
          locale={{ emptyText: <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} description="暂无文档，请上传文件" /> }}
          columns={[
            { title: "文件名", dataIndex: "filename", ellipsis: true },
            { title: "类型", dataIndex: "file_type", width: 120 },
            {
              title: "状态",
              dataIndex: "status",
              width: 140,
              render: (value) => <Tag color={value === "completed" ? "green" : value === "failed" ? "red" : "blue"}>{value}</Tag>
            },
            { title: "Chunk 数量", dataIndex: "chunk_count", width: 130 },
            {
              title: "操作",
              width: 230,
              render: (_, record) => (
                <Space>
                  <Button size="small" icon={<EyeOutlined />} onClick={() => showChunks(record)} disabled={record.chunk_count === 0}>
                    查看切分
                  </Button>
                  <Popconfirm title="删除文件" description="将同时删除该文件的全部分片，确定删除吗？" onConfirm={() => deleteDocument(record)}>
                    <Button size="small" danger icon={<DeleteOutlined />}>
                      删除
                    </Button>
                  </Popconfirm>
                </Space>
              )
            }
          ]}
        />
      </Card>

      <Drawer
        title={chunkDoc ? `${chunkDoc.filename} · Chunk 明细` : "Chunk 明细"}
        width={720}
        open={chunkOpen}
        onClose={() => setChunkOpen(false)}
        extra={
          <Popconfirm title="清空分片" description="只删除该文档的分片，文件记录会保留，确定清空吗？" onConfirm={clearChunks} disabled={!chunks.length}>
            <Button danger icon={<DeleteOutlined />} disabled={!chunks.length}>
              清空分片
            </Button>
          </Popconfirm>
        }
      >
        {chunks.length === 0 ? (
          <Empty description="暂无 Chunk 内容" />
        ) : (
          <Space direction="vertical" size={12} className="chunk-list">
            {chunks.map((chunk, index) => (
              <div className="chunk-card" key={chunk.id}>
                <div className="chunk-meta">
                  <Typography.Text strong>Chunk {index + 1}</Typography.Text>
                  <Space size={8}>
                    <Tag>第 {chunk.page_no} 页</Tag>
                    <Tag>{chunk.token_count} 字符</Tag>
                    <Popconfirm title="删除分片" description="确定删除这个 Chunk 吗？" onConfirm={() => deleteChunk(chunk)}>
                      <Button size="small" danger type="text" icon={<DeleteOutlined />}>
                        删除
                      </Button>
                    </Popconfirm>
                  </Space>
                </div>
                <Typography.Paragraph className="chunk-content">{chunk.content}</Typography.Paragraph>
              </div>
            ))}
          </Space>
        )}
      </Drawer>

      <Modal title="创建知识库" open={open} onCancel={() => setOpen(false)} onOk={() => form.submit()}>
        <Form form={form} layout="vertical" onFinish={async (values) => { await apiPost("/knowledge-bases", values); setOpen(false); form.resetFields(); load(); }}>
          <Form.Item name="name" label="名称" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="description" label="描述">
            <Input.TextArea />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
}
