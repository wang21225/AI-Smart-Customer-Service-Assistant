import { createBrowserRouter, Navigate } from "react-router-dom";

import { AppLayout } from "../layouts/AppLayout";
import { ChatPage } from "../pages/ChatPage";
import { DashboardPage } from "../pages/DashboardPage";
import { KnowledgePage } from "../pages/KnowledgePage";
import { RetrievalPage } from "../pages/RetrievalPage";
import { TicketsPage } from "../pages/TicketsPage";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <AppLayout />,
    children: [
      { index: true, element: <Navigate to="/chat" replace /> },
      { path: "dashboard", element: <DashboardPage /> },
      { path: "chat", element: <ChatPage /> },
      { path: "knowledge", element: <KnowledgePage /> },
      { path: "retrieval", element: <RetrievalPage /> },
      { path: "tickets", element: <TicketsPage /> }
    ]
  }
]);
