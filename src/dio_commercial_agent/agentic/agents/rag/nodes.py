import logging

from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore
from langchain_core.language_models import BaseChatModel

from ..base import BaseNode
from .state import RAGState
from ..utils import format_documents, create_llm_chain


class RetrieveNode(BaseNode):
    name = "retrieve"

    def __init__(self, vector_store: VectorStore, top_k: int) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.retriever = vector_store.as_retriever(k=top_k)

    async def __call__(self, state: RAGState) -> dict[str, list[Document]]:
        self.logger.info("---RETRIEVE DOCUMENTS---")
        documents = await self.retriever.ainvoke(state["question"])
        return {"documents": documents}


class GenerateNode(BaseNode):
    name = "generate"

    def __init__(self, model: BaseChatModel, template: str) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.llm_chain = create_llm_chain(template, model)

    async def __call__(self, state: RAGState) -> dict[str, str]:
        self.logger.info("---GENERATE ANSWER---")
        context = format_documents(state["documents"])
        answer = await self.llm_chain.ainvoke({
            "question": state["question"],
            "context": context
        })
        return {"answer": answer}
