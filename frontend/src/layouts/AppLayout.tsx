import {
  BarChartOutlined,
  DatabaseOutlined,
  MessageOutlined,
  SearchOutlined,
  SettingOutlined,
  ToolOutlined
} from "@ant-design/icons";
import { Layout, Menu, Typography } from "antd";
import { Outlet, useLocation, useNavigate } from "react-router-dom";

const { Header, Sider, Content } = Layout;

export function AppLayout() {
  const navigate = useNavigate();
  const location = useLocation();
  return (
    <Layout className="app-shell">
      <Sider width={236} className="sidebar">
        <div className="brand">
          <div className="brand-mark">AI</div>
          <div>
            <Typography.Title level={4}>智能客服</Typography.Title>
            <span>Customer Service</span>
          </div>
        </div>
        <Menu
          mode="inline"
          selectedKeys={[location.pathname]}
          onClick={(item) => navigate(item.key)}
          items={[
            { key: "/dashboard", icon: <BarChartOutlined />, label: "工作台" },
            { key: "/chat", icon: <MessageOutlined />, label: "智能客服" },
            { key: "/knowledge", icon: <DatabaseOutlined />, label: "知识库" },
            { key: "/retrieval", icon: <SearchOutlined />, label: "检索测试" },
            { key: "/tickets", icon: <ToolOutlined />, label: "客服工单" },
            { key: "/settings", icon: <SettingOutlined />, label: "系统设置", disabled: true }
          ]}
        />
      </Sider>
      <Layout>
        <Header className="topbar">
          <div>
            <Typography.Text strong>AI 智能客服系统</Typography.Text>
            <Typography.Text type="secondary">百炼大模型 · LangGraph · RAG</Typography.Text>
          </div>
        </Header>
        <Content className="content">
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  );
}
