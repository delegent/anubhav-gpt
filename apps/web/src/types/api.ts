export type Role = "user" | "assistant" | "system";

export interface Message {
  id: string;
  role: Role;
  content: string;
  status: "pending" | "completed" | "failed";
  created_at: string;
}

export interface ConversationSummary {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
}

export interface ConversationDetail extends ConversationSummary {
  messages: Message[];
}

export interface ChatResponse {
  conversation_id: string;
  message_id: string;
  role: "assistant";
  content: string;
  created_at: string;
}
