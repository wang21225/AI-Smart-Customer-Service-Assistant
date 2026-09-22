export interface Conversation {
  id: number;
  title: string;
  status: string;
  last_intent?: string;
  need_human: boolean;
  created_at: string;
  updated_at: string;
}

export interface Message {
  id?: number;
  conversation_id?: number;
  role: "user" | "assistant" | "system" | "tool";
  content: string;
  intent?: string;
  sources?: SourceInfo[];
  created_at?: string;
}

export interface SourceInfo {
  document_id?: number;
  document_name: string;
  page_no: number;
  score: number;
  snippet: string;
}

export interface KnowledgeBase {
  id: number;
  name: string;
  description?: string;
  is_default: boolean;
}

export interface KnowledgeDocument {
  id: number;
  knowledge_base_id: number;
  filename: string;
  file_type: string;
  status: string;
  chunk_count: number;
  error_message?: string;
}

export interface DocumentChunk {
  id: number;
  document_id: number;
  page_no: number;
  content: string;
  token_count: number;
  score?: number;
  created_at: string;
}
