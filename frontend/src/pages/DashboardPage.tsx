import { Card, Col, Empty, Row, Statistic, Typography } from "antd";
import type { EChartsOption } from "echarts";
import ReactECharts from "echarts-for-react";
import { useEffect, useMemo, useState } from "react";

import { apiGet } from "../api/client";

interface Stats {
  todayConversations: number;
  todayUsers: number;
  autoResolveRate: number;
  humanTransfers: number;
  avgResponseTime: string | null;
  satisfaction: number;
  knowledgeHitRate: number;
  likes: number;
  dislikes: number;
}

interface TrendData {
  dates: string[];
  sessions: number[];
  intents: Array<{ name: string; value: number }>;
}

export function DashboardPage() {
  const [stats, setStats] = useState<Stats>();
  const [trends, setTrends] = useState<TrendData>();

  useEffect(() => {
    apiGet<Stats>("/dashboard/statistics").then(setStats);
    apiGet<TrendData>("/dashboard/trends").then(setTrends);
  }, []);

  const sessionOption = useMemo<EChartsOption>(
    () => ({
      grid: { left: 48, right: 24, top: 32, bottom: 36 },
      tooltip: { trigger: "axis" as const },
      xAxis: {
        type: "category" as const,
        data: trends?.dates || [],
        axisTick: { show: false },
      },
      yAxis: {
        type: "value" as const,
        minInterval: 1,
        splitLine: { lineStyle: { color: "#eef1f6" } },
      },
      series: [
        {
          type: "bar" as const,
          data: trends?.sessions || [],
          barMaxWidth: 42,
          itemStyle: { color: "#5b5ff2", borderRadius: [6, 6, 0, 0] },
        },
      ],
    }),
    [trends],
  );

  const intentOption = useMemo<EChartsOption>(
    () => ({
      tooltip: { trigger: "item" as const },
      legend: { bottom: 0, left: "center" },
      series: [
        {
          type: "pie" as const,
          radius: ["48%", "72%"],
          center: ["50%", "44%"],
          avoidLabelOverlap: true,
          data: trends?.intents || [],
        },
      ],
    }),
    [trends],
  );

  const hasIntentData = Boolean(trends?.intents?.length);

  return (
    <div className="page-stack">
      <Typography.Title level={3}>工作台</Typography.Title>
      <Row gutter={[16, 16]}>
        <Col xs={12} md={6}>
          <Card>
            <Statistic title="今日会话数" value={stats?.todayConversations || 0} />
          </Card>
        </Col>
        <Col xs={12} md={6}>
          <Card>
            <Statistic title="AI 自动解决率" value={stats?.autoResolveRate || 0} suffix="%" />
          </Card>
        </Col>
        <Col xs={12} md={6}>
          <Card>
            <Statistic title="转人工数量" value={stats?.humanTransfers || 0} />
          </Card>
        </Col>
        <Col xs={12} md={6}>
          <Card>
            <Statistic title="知识库命中率" value={stats?.knowledgeHitRate || 0} suffix="%" />
          </Card>
        </Col>
      </Row>
      <Row gutter={[16, 16]}>
        <Col xs={24} lg={14}>
          <Card title="会话趋势">
            <ReactECharts option={sessionOption} style={{ height: 320 }} />
          </Card>
        </Col>
        <Col xs={24} lg={10}>
          <Card title="意图分布">
            {hasIntentData ? (
              <ReactECharts option={intentOption} style={{ height: 320 }} />
            ) : (
              <Empty description="暂无意图数据" style={{ height: 320, paddingTop: 96 }} />
            )}
          </Card>
        </Col>
      </Row>
    </div>
  );
}
