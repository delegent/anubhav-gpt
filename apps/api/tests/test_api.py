async def test_health(client):
    response = await client.get("/api/v1/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_conversation_and_chat_flow(client):
    created = await client.post("/api/v1/conversations", json={"title": "New conversation"})
    assert created.status_code == 201
    conversation_id = created.json()["id"]

    chat = await client.post(
        "/api/v1/chat",
        json={"conversation_id": conversation_id, "message": "Explain state graphs."},
    )
    assert chat.status_code == 200
    assert chat.json()["role"] == "assistant"
    assert "AnubhavGPT response" in chat.json()["content"]

    detail = await client.get(f"/api/v1/conversations/{conversation_id}")
    assert len(detail.json()["messages"]) == 2


async def test_stream_event_order(client):
    created = await client.post("/api/v1/conversations", json={"title": "New conversation"})
    conversation_id = created.json()["id"]
    async with client.stream(
        "POST",
        "/api/v1/chat/stream",
        json={"conversation_id": conversation_id, "message": "Stream this."},
    ) as response:
        body = "".join([chunk async for chunk in response.aiter_text()])
    assert response.status_code == 200
    assert body.index("event: metadata") < body.index("event: delta") < body.index("event: done")


async def test_error_envelope(client):
    response = await client.post("/api/v1/chat", json={"conversation_id": "nope", "message": ""})
    assert response.status_code == 422
    payload = response.json()
    assert payload["error"]["code"] == "VALIDATION_ERROR"
    assert payload["error"]["request_id"]
