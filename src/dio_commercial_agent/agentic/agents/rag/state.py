from typing_extensions import TypedDict

from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, AIMessage


class RAGState(TypedDict):
    question: str
    documents: list[Document]
    answer: str
