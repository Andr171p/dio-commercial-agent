from langgraph.graph.graph import CompiledGraph
from langgraph.graph import START, END, StateGraph

from langchain_core.vectorstores import VectorStore
from langchain_core.language_models import BaseChatModel

from .state import RAGState
from .nodes import RetrieveNode, GenerateNode


def create_rag_agent(
        vector_store: VectorStore,
        top_k: int,
        model: BaseChatModel,
        template: str
) -> CompiledGraph:
    workflow = (
        StateGraph(RAGState)
        .add_node("retrieve", RetrieveNode(vector_store, top_k))
        .add_node("generate", GenerateNode(model, template))
        .add_edge(START, "retrieve")
        .add_edge("retrieve", "generate")
        .add_edge("generate", END)
    )
    return workflow.compile()
