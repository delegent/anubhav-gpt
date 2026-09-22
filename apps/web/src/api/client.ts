import type { ConversationDetail, ConversationSummary } from "../types/api";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: { "content-type": "application/json", ...(init?.headers ?? {}) },
  });
  if (!response.ok) {
    const payload = await response.json().catch(() => null);
    throw new Error(payload?.error?.message ?? "Request failed.");
  }
  if (response.status === 204) return undefined as T;
  return response.json() as Promise<T>;
}

export const api = {
  listConversations: () => request<ConversationSummary[]>("/conversations"),
  createConversation: (title = "New conversation") =>
    request<ConversationDetail>("/conversations", {
      method: "POST",
      body: JSON.stringify({ title }),
    }),
  getConversation: (id: string) => request<ConversationDetail>(`/conversations/${id}`),
  renameConversation: (id: string, title: string) =>
    request<ConversationSummary>(`/conversations/${id}`, {
      method: "PATCH",
      body: JSON.stringify({ title }),
    }),
  deleteConversation: (id: string) => request<void>(`/conversations/${id}`, { method: "DELETE" }),
  streamChat: async (
    conversationId: string,
    message: string,
    onDelta: (content: string) => void,
    signal: AbortSignal,
  ) => {
    const response = await fetch(`${API_BASE_URL}/chat/stream`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ conversation_id: conversationId, message }),
      signal,
    });
    if (!response.ok || !response.body) {
      const payload = await response.json().catch(() => null);
      throw new Error(payload?.error?.message ?? "The assistant is unavailable.");
    }
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";
    for (;;) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const events = buffer.split("\n\n");
      buffer = events.pop() ?? "";
      for (const event of events) {
        const lines = event.split("\n");
        const eventName = lines.find((line) => line.startsWith("event: "))?.slice(7);
        const dataLine = lines.find((line) => line.startsWith("data: "))?.slice(6);
        if (eventName === "delta" && dataLine) {
          onDelta(JSON.parse(dataLine).content);
        }
        if (eventName === "error" && dataLine) {
          throw new Error(JSON.parse(dataLine).message);
        }
      }
    }
  },
};
