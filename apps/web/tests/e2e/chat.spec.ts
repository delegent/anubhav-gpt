import { test, expect } from "@playwright/test";

test("critical streamed chat flow persists after refresh", async ({ page }) => {
  const conversation = {
    id: "0195cc33-bcc2-7ec4-a9f4-7e0a7765bb4a",
    title: "Explain LangGraph state.",
    created_at: "2026-09-22T14:00:00Z",
    updated_at: "2026-09-22T14:00:00Z",
  };
  const messages = [
    {
      id: "user-1",
      role: "user",
      content: "Explain LangGraph state with a practical backend example.",
      status: "completed",
      created_at: "2026-09-22T14:00:00Z",
    },
    {
      id: "assistant-1",
      role: "assistant",
      content: "### AnubhavGPT response\n\nA streamed fake answer.",
      status: "completed",
      created_at: "2026-09-22T14:00:01Z",
    },
  ];

  await page.route("**/api/v1/conversations", async (route) => {
    if (route.request().method() === "POST") {
      await route.fulfill({ json: { ...conversation, messages: [] }, status: 201 });
      return;
    }
    await route.fulfill({ json: [conversation] });
  });
  await page.route(`**/api/v1/conversations/${conversation.id}`, async (route) => {
    await route.fulfill({ json: { ...conversation, messages } });
  });
  await page.route("**/api/v1/chat/stream", async (route) => {
    await route.fulfill({
      status: 200,
      headers: { "content-type": "text/event-stream" },
      body:
        'event: metadata\ndata: {"conversation_id":"0195cc33-bcc2-7ec4-a9f4-7e0a7765bb4a","message_id":"assistant-1"}\n\n' +
        'event: delta\ndata: {"content":"### AnubhavGPT response\\n\\nA streamed fake answer."}\n\n' +
        'event: done\ndata: {"finish_reason":"stop"}\n\n',
    });
  });

  await page.goto("/");
  await expect(page.getByText("Ask for a clear technical resolution.")).toBeVisible();
  await page.getByText("Explain LangGraph state with a practical backend example.").click();
  await expect(page.getByText("A streamed fake answer.")).toBeVisible();
  await page.reload();
  await page.getByText("Explain LangGraph state.").click();
  await expect(page.getByText("A streamed fake answer.")).toBeVisible();
});
