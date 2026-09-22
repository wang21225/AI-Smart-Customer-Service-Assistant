import { Card, Table, Tag } from "antd";
import { useEffect, useState } from "react";

import { apiGet } from "../api/client";

interface Ticket {
  id: number;
  ticket_no: string;
  category: string;
  content: string;
  status: string;
  priority: string;
  created_at: string;
}

export function TicketsPage() {
  const [items, setItems] = useState<Ticket[]>([]);
  useEffect(() => {
    apiGet<Ticket[]>("/tickets").then(setItems);
  }, []);
  return (
    <Card title="客服工单">
      <Table rowKey="id" dataSource={items} columns={[
        { title: "工单编号", dataIndex: "ticket_no" },
        { title: "类型", dataIndex: "category" },
        { title: "内容", dataIndex: "content" },
        { title: "状态", dataIndex: "status", render: (value) => <Tag color={value === "open" ? "red" : "green"}>{value}</Tag> },
        { title: "优先级", dataIndex: "priority" }
      ]} />
    </Card>
  );
}
