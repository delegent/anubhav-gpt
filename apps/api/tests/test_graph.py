from langchain_core.messages import AIMessage

from app.db.repositories import title_from_message
from app.graph.nodes import normalize_text


def test_normalize_text_from_content_blocks():
    message = AIMessage(content=[{"type": "text", "text": "hello"}, {"type": "text", "text": "world"}])
    assert normalize_text(message) == "hello\nworld"


def test_title_generation_is_deterministic():
    assert title_from_message("  Fix   the deploy   ") == "Fix the deploy"
    assert title_from_message("x" * 80).endswith("...")
