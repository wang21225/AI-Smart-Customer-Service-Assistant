import { DatabaseOutlined, SearchOutlined, ThunderboltOutlined } from "@ant-design/icons";
import { Button, Card, Empty, Form, Input, InputNumber, Select, Space, Tag, Typography } from "antd";
import { useCallback, useEffect, useState } from "react";

import { apiGet, apiPost } from "../api/client";
import type { KnowledgeBase, SourceInfo } from "../types";

interface RetrievalForm {
  knowledge_base_id: number;
  query: string;
  top_k: number;
}

export function RetrievalPage() {
  const [form] = Form.useForm<RetrievalForm>();
  const [bases, setBases] = useState<KnowledgeBase[]>([]);
  const [results, setResults] = useState<SourceInfo[]>([]);
  const [lastQuery, setLastQuery] = useState("");
  const [loading, setLoading] = useState(false);

  const loadBases = useCallback(async () => {
    const data = await apiGet<KnowledgeBase[]>("/knowledge-bases");
    setBases(data);
    const currentId = form.getFieldValue("knowledge_base_id");
    const currentStillExists = data.some((item) => item.id === currentId);
    if (currentStillExists) return;
    form.setFieldValue("knowledge_base_id", data[0]?.id);
    setResults([]);
    setLastQuery("");
  }, [form]);

  useEffect(() => {
    loadBases();
    const refresh = () => loadBases();
    window.addEventListener("focus", refresh);
    document.addEventListener("visibilitychange", refresh);
    return () => {
      window.removeEventListener("focus", refresh);
      document.removeEventListener("visibilitychange", refresh);
    };
  }, [loadBases]);

  const runRetrieval = async (values: RetrievalForm) => {
    setLoading(true);
    try {
      const data = await apiPost<{ results: SourceInfo[] }>("/retrieval/test", values);
      setResults(data.results);
      setLastQuery(values.query);
    } finally {
      setLoading(false);
    }
  };

  const examples = ["商品签收后几天可以退货？", "软件激活后还能退款吗？", "退款审核通过后多久能到账？"];

  return (
    <div className="retrieval-page">
      <Card className="retrieval-search-card">
        <div className="retrieval-header">
          <div>
            <Typography.Title level={3}>检索测试</Typography.Title>
            <Typography.Text type="secondary">调试知识库召回效果，查看问题命中的文档、页码、相关度和片段。</Typography.Text>
          </div>
          <Tag icon={<ThunderboltOutlined />} color="blue">RAG Recall Lab</Tag>
        </div>

        <Form<RetrievalForm>
          form={form}
          initialValues={{ top_k: 3 }}
          onFinish={runRetrieval}
          onValuesChange={(changedValues) => {
            if ("query" in changedValues && !changedValues.query) {
              setResults([]);
              setLastQuery("");
            }
          }}
        >
          <div className="retrieval-toolbar">
            <Form.Item name="knowledge_base_id" rules={[{ required: true, message: "请选择知识库" }]}>
              <Select
                size="large"
                placeholder="选择知识库"
                options={bases.map((item) => ({ label: item.name, value: item.id }))}
                suffixIcon={<DatabaseOutlined />}
                onDropdownVisibleChange={(open) => {
                  if (open) loadBases();
                }}
              />
            </Form.Item>
            <Form.Item name="query" rules={[{ required: true, message: "请输入检索问题" }]}>
              <Input size="large" placeholder="输入用户可能会问的问题" allowClear />
            </Form.Item>
            <Form.Item name="top_k">
              <InputNumber min={1} max={3} size="large" addonBefore="Top K" />
            </Form.Item>
            <Button type="primary" size="large" htmlType="submit" icon={<SearchOutlined />} loading={loading}>
              检索
            </Button>
          </div>
        </Form>

        <Space wrap className="retrieval-examples">
          <Typography.Text type="secondary">快速测试：</Typography.Text>
          {examples.map((item) => (
            <Button key={item} size="small" onClick={() => form.setFieldValue("query", item)}>
              {item}
            </Button>
          ))}
        </Space>
      </Card>

      <Card
        className="retrieval-results-card"
        title={
          <div className="document-card-title">
            <Typography.Text strong>召回结果</Typography.Text>
            <Typography.Text type="secondary">{lastQuery ? `当前问题：${lastQuery}` : "提交问题后查看召回片段"}</Typography.Text>
          </div>
        }
        extra={<Tag color={results.length ? "green" : "default"}>{results.length} 条命中</Tag>}
      >
        {results.length === 0 ? (
          <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} description="暂无召回结果" className="retrieval-empty" />
        ) : (
          <div className="retrieval-result-list">
            {results.map((item, index) => (
              <div className="retrieval-result-card" key={`${item.document_name}-${item.page_no}-${item.score}-${index}`}>
                <div className="retrieval-result-meta">
                  <Space size={8} wrap>
                    <Tag color="blue">#{index + 1}</Tag>
                    <Typography.Text strong>{item.document_name}</Typography.Text>
                    <Tag>第 {item.page_no} 页</Tag>
                  </Space>
                  <div className="score-pill">
                    <span>相关度</span>
                    <strong>{Math.round(item.score * 100)}%</strong>
                  </div>
                </div>
                <Typography.Paragraph className="retrieval-snippet">{item.snippet}</Typography.Paragraph>
              </div>
            ))}
          </div>
        )}
      </Card>
    </div>
  );
}
