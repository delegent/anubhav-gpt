import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Menu } from "lucide-react";
import { useRef, useState } from "react";
import { api } from "../api/client";
import { MarkdownMessage } from "../components/MarkdownMessage";
import { ChatComposer } from "../features/chat/ChatComposer";
import { ConversationSidebar } from "../features/chat/ConversationSidebar";
import type { Message } from "../types/api";

const starters = [
  "Explain LangGraph state with a practical backend example.",
  "Help me debug a production latency spike.",
  "Compare FastAPI service and repository boundaries.",
  "Draft a safe incident resolution checklist.",
];

export function ChatPage() {
  const queryClient = useQueryClient();
  const [selectedId, setSelectedId] = useState<string>();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [localMessages, setLocalMessages] = useState<Message[]>([]);
  const [error, setError] = useState("");
  const abortRef = useRef<AbortController | null>(null);

  const conversations = useQuery({ queryKey: ["conversations"], queryFn: api.listConversations });
  const detail = useQuery({
    queryKey: ["conversation", selectedId],
    queryFn: () => api.getConversation(selectedId!),
    enabled: Boolean(selectedId),
  });
  const create = useMutation({
    mutationFn: () => api.createConversation(),
    onSuccess: (conversation) => {
      setSelectedId(conversation.id);
      setLocalMessages(conversation.messages);
      queryClient.invalidateQueries({ queryKey: ["conversations"] });
    },
  });
  const remove = useMutation({
    mutationFn: api.deleteConversation,
    onSuccess: (_, id) => {
      if (selectedId === id) setSelectedId(undefined);
      queryClient.invalidateQueries({ queryKey: ["conversations"] });
    },
  });

  const messages = selectedId
    ? localMessages.length
      ? localMessages
      : (detail.data?.messages ?? [])
    : [];
  const streaming = Boolean(abortRef.current);

  async function ensureConversation() {
    if (selectedId) return selectedId;
    const conversation = await api.createConversation();
    setSelectedId(conversation.id);
    queryClient.invalidateQueries({ queryKey: ["conversations"] });
    return conversation.id;
  }

  async function send(message: string) {
    setError("");
    const conversationId = await ensureConversation();
    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: message.trim(),
      status: "completed",
      created_at: new Date().toISOString(),
    };
    const assistantMessage: Message = {
      id: crypto.randomUUID(),
      role: "assistant",
      content: "",
      status: "pending",
      created_at: new Date().toISOString(),
    };
    setLocalMessages((current) => [
      ...(current.length ? current : (detail.data?.messages ?? [])),
      userMessage,
      assistantMessage,
    ]);
    const abort = new AbortController();
    abortRef.current = abort;
    try {
      await api.streamChat(
        conversationId,
        message,
        (delta) => {
          setLocalMessages((current) =>
            current.map((item) =>
              item.id === assistantMessage.id
                ? { ...item, content: item.content + delta, status: "completed" }
                : item,
            ),
          );
        },
        abort.signal,
      );
      queryClient.invalidateQueries({ queryKey: ["conversation", conversationId] });
      queryClient.invalidateQueries({ queryKey: ["conversations"] });
    } catch (exc) {
      setError(exc instanceof Error ? exc.message : "Network error.");
      throw exc;
    } finally {
      abortRef.current = null;
    }
  }

  return (
    <div className="flex h-screen overflow-hidden bg-graphite text-slate-100">
      <div
        className={`${sidebarOpen ? "fixed inset-0 z-20 block" : "hidden"} md:relative md:block`}
      >
        <ConversationSidebar
          conversations={conversations.data ?? []}
          selectedId={selectedId}
          onNew={() => create.mutate()}
          onSelect={(id) => {
            setSelectedId(id);
            setLocalMessages([]);
            setSidebarOpen(false);
          }}
          onDelete={(id) => {
            if (window.confirm("Delete this conversation?")) remove.mutate(id);
          }}
        />
      </div>
      <main className="flex min-w-0 flex-1 flex-col">
        <header className="flex items-center gap-3 border-b border-line px-4 py-3 md:hidden">
          <button
            aria-label="Open conversations"
            onClick={() => setSidebarOpen(true)}
            className="rounded-md border border-line p-2"
          >
            <Menu size={18} />
          </button>
          <span className="font-semibold">AnubhavGPT</span>
        </header>
        <section className="flex-1 overflow-y-auto px-4 py-8">
          <div className="mx-auto max-w-3xl">
            {!selectedId && messages.length === 0 ? (
              <div className="flex min-h-[70vh] flex-col justify-center">
                <p className="mb-3 text-sm font-medium text-accent">
                  Software-engineering assistant
                </p>
                <h2 className="mb-4 text-4xl font-semibold tracking-normal text-white">
                  Ask for a clear technical resolution.
                </h2>
                <div className="grid gap-3 sm:grid-cols-2">
                  {starters.map((starter) => (
                    <button
                      key={starter}
                      onClick={() => send(starter)}
                      className="rounded-lg border border-line bg-panel p-4 text-left text-sm text-slate-300 hover:border-accent"
                    >
                      {starter}
                    </button>
                  ))}
                </div>
              </div>
            ) : detail.isLoading ? (
              <p className="text-slate-400">Loading conversation...</p>
            ) : (
              <div className="space-y-7">
                {messages.map((message) => (
                  <article
                    key={message.id}
                    className={message.role === "user" ? "ml-auto max-w-2xl" : "max-w-3xl"}
                  >
                    <div
                      className={
                        message.role === "user"
                          ? "rounded-lg bg-accent px-4 py-3 text-white"
                          : "border-l border-line pl-4 text-slate-100"
                      }
                    >
                      {message.role === "assistant" ? (
                        <MarkdownMessage content={message.content || "Thinking..."} />
                      ) : (
                        message.content
                      )}
                    </div>
                  </article>
                ))}
              </div>
            )}
            {error ? (
              <p
                role="alert"
                className="mt-4 rounded-md border border-red-500/40 bg-red-500/10 p-3 text-sm text-red-200"
              >
                {error}
              </p>
            ) : null}
          </div>
        </section>
        <ChatComposer
          streaming={streaming}
          disabled={!navigator.onLine}
          onSend={send}
          onStop={() => abortRef.current?.abort()}
        />
      </main>
    </div>
  );
}
