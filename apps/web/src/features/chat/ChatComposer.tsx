import { Send, Square } from "lucide-react";
import { FormEvent, useState } from "react";

export function ChatComposer({
  disabled,
  streaming,
  onSend,
  onStop,
}: {
  disabled?: boolean;
  streaming: boolean;
  onSend: (message: string) => Promise<void>;
  onStop: () => void;
}) {
  const [message, setMessage] = useState("");
  const canSend = message.trim().length > 0 && !disabled && !streaming;

  async function submit(event: FormEvent) {
    event.preventDefault();
    if (!canSend) return;
    const next = message;
    setMessage("");
    try {
      await onSend(next);
    } catch {
      setMessage(next);
    }
  }

  return (
    <form onSubmit={submit} className="border-t border-line bg-graphite/95 p-4">
      <div className="mx-auto flex max-w-3xl items-end gap-3 rounded-lg border border-line bg-panel p-2">
        <textarea
          aria-label="Message"
          rows={2}
          value={message}
          onChange={(event) => setMessage(event.target.value)}
          placeholder="Ask about a production issue, architecture tradeoff, or LangChain concept..."
          className="max-h-40 min-h-12 flex-1 resize-none bg-transparent px-2 py-2 text-sm text-slate-100 placeholder:text-slate-500 focus:outline-none"
        />
        {streaming ? (
          <button
            type="button"
            aria-label="Stop streaming"
            onClick={onStop}
            className="rounded-md bg-slate-700 p-3"
          >
            <Square size={18} />
          </button>
        ) : (
          <button
            type="submit"
            aria-label="Send message"
            disabled={!canSend}
            className="rounded-md bg-accent p-3 text-white disabled:cursor-not-allowed disabled:opacity-40"
          >
            <Send size={18} />
          </button>
        )}
      </div>
    </form>
  );
}
