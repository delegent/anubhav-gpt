import { Plus, Trash2 } from "lucide-react";
import type { ConversationSummary } from "../../types/api";

export function ConversationSidebar({
  conversations,
  selectedId,
  onNew,
  onSelect,
  onDelete,
}: {
  conversations: ConversationSummary[];
  selectedId?: string;
  onNew: () => void;
  onSelect: (id: string) => void;
  onDelete: (id: string) => void;
}) {
  return (
    <aside className="flex h-full w-full flex-col border-r border-line bg-[#12141b] md:w-80">
      <div className="flex items-center justify-between border-b border-line p-4">
        <h1 className="text-lg font-semibold tracking-normal">AnubhavGPT</h1>
        <button
          aria-label="New conversation"
          onClick={onNew}
          className="rounded-md border border-line p-2 text-slate-200"
        >
          <Plus size={18} />
        </button>
      </div>
      <nav className="flex-1 overflow-y-auto p-3">
        {conversations.length === 0 ? (
          <p className="px-2 py-6 text-sm text-slate-500">No conversations yet.</p>
        ) : (
          conversations.map((conversation) => (
            <div key={conversation.id} className="group flex items-center gap-2">
              <button
                className={`mb-1 min-w-0 flex-1 rounded-md px-3 py-2 text-left text-sm ${
                  selectedId === conversation.id
                    ? "bg-accent/20 text-white"
                    : "text-slate-300 hover:bg-white/5"
                }`}
                onClick={() => onSelect(conversation.id)}
              >
                <span className="block truncate">{conversation.title}</span>
              </button>
              <button
                aria-label={`Delete ${conversation.title}`}
                onClick={() => onDelete(conversation.id)}
                className="mb-1 rounded-md p-2 text-slate-500 opacity-100 hover:text-red-300 md:opacity-0 md:group-hover:opacity-100"
              >
                <Trash2 size={16} />
              </button>
            </div>
          ))
        )}
      </nav>
    </aside>
  );
}
