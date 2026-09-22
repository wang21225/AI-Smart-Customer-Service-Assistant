import { create } from "zustand";

import { apiDelete, apiGet } from "../api/client";
import type { Conversation, Message, SourceInfo } from "../types";

interface ChatState {
  conversations: Conversation[];
  messages: Message[];
  activeSessionId?: number;
  intent?: string;
  sources: SourceInfo[];
  statusText: string;
  loading: boolean;
  loadConversations: () => Promise<void>;
  openConversation: (id: number) => Promise<void>;
  deleteConversation: (id: number) => Promise<void>;
  newConversation: () => void;
  sendMessage: (content: string) => Promise<void>;
}

export const useChatStore = create<ChatState>((set, get) => ({
  conversations: [],
  messages: [],
  sources: [],
  statusText: "",
  loading: false,
  async loadConversations() {
    set({ conversations: await apiGet<Conversation[]>("/conversations") });
  },
  async openConversation(id) {
    const messages = await apiGet<Message[]>(`/conversations/${id}/messages`);
    set({ activeSessionId: id, messages, sources: messages.at(-1)?.sources || [] });
  },
  async deleteConversation(id) {
    await apiDelete(`/conversations/${id}`);
    const conversations = await apiGet<Conversation[]>("/conversations");
    if (get().activeSessionId === id) {
      set({
        conversations,
        activeSessionId: undefined,
        messages: [],
        sources: [],
        intent: undefined,
        statusText: ""
      });
      return;
    }
    set({ conversations });
  },
  newConversation() {
    set({ activeSessionId: undefined, messages: [], sources: [], intent: undefined, statusText: "" });
  },
  async sendMessage(content) {
    const userMessage: Message = { role: "user", content, created_at: new Date().toISOString() };
    const assistant: Message = { role: "assistant", content: "", created_at: new Date().toISOString() };
    set({ messages: [...get().messages, userMessage, assistant], loading: true, statusText: "正在发送问题..." });
    const response = await fetch("/api/chat/stream", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: content, session_id: get().activeSessionId })
    });
    const reader = response.body?.getReader();
    if (!reader) {
      set({ loading: false, statusText: "连接失败" });
      return;
    }
    const decoder = new TextDecoder();
    let buffer = "";
    let answer = "";
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const parts = buffer.split("\n\n");
      buffer = parts.pop() || "";
      for (const part of parts) {
        const event = part.match(/^event: (.+)$/m)?.[1];
        const data = part.match(/^data: (.+)$/m)?.[1];
        if (!data) continue;
        const json = JSON.parse(data);
        if (event === "status") set({ statusText: json.status });
        if (event === "token") {
          answer += json.token;
          const next = [...get().messages];
          next[next.length - 1] = { ...assistant, content: answer };
          set({ messages: next });
        }
        if (event === "done") {
          const doneData = json;
          set({
            activeSessionId: doneData.session_id,
            intent: doneData.intent,
            sources: doneData.sources || [],
            statusText: "回答完成",
            loading: false
          });
          await get().loadConversations();
        }
      }
    }
    set({ loading: false });
  }
}));
