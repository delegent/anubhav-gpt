import { Check, Copy } from "lucide-react";
import { useState } from "react";
import ReactMarkdown from "react-markdown";
import rehypeSanitize from "rehype-sanitize";
import remarkGfm from "remark-gfm";

export function MarkdownMessage({ content }: { content: string }) {
  return (
    <ReactMarkdown
      className="prose prose-invert max-w-none prose-pre:bg-[#0b0c10] prose-pre:border prose-pre:border-line"
      remarkPlugins={[remarkGfm]}
      rehypePlugins={[rehypeSanitize]}
      components={{
        code({ className, children }) {
          const code = String(children).replace(/\n$/, "");
          const isBlock = className?.includes("language-");
          if (!isBlock) return <code className={className}>{children}</code>;
          return <CodeBlock code={code} />;
        },
      }}
    >
      {content}
    </ReactMarkdown>
  );
}

function CodeBlock({ code }: { code: string }) {
  const [copied, setCopied] = useState(false);
  return (
    <div className="group relative">
      <button
        aria-label="Copy code"
        className="absolute right-2 top-2 rounded-md border border-line bg-panel p-2 text-slate-300 opacity-0 transition group-hover:opacity-100"
        onClick={() => {
          navigator.clipboard.writeText(code);
          setCopied(true);
          window.setTimeout(() => setCopied(false), 1200);
        }}
      >
        {copied ? <Check size={16} /> : <Copy size={16} />}
      </button>
      <pre>
        <code>{code}</code>
      </pre>
    </div>
  );
}
