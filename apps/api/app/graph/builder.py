from langgraph.graph import END, START, StateGraph

from app.core.config import Settings
from app.graph.nodes import (
    ChatModel,
    assistant_model_node,
    persist_result_node,
    validate_context_node,
)
from app.graph.state import GraphState


def build_graph(model: ChatModel, settings: Settings):
    async def assistant_node(state: GraphState) -> GraphState:
        return await assistant_model_node(state, model, settings)

    graph = StateGraph(GraphState)
    graph.add_node("validate_context", validate_context_node)
    graph.add_node("assistant_model", assistant_node)
    graph.add_node("persist_result", persist_result_node)
    graph.add_edge(START, "validate_context")
    graph.add_edge("validate_context", "assistant_model")
    graph.add_edge("assistant_model", "persist_result")
    graph.add_edge("persist_result", END)
    return graph.compile()
