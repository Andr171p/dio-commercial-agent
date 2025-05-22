from typing import Sequence, Type

import logging

from pydantic import BaseModel

from langchain_core.runnables import Runnable
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser

from .templates import SUMMARIZATION_TEMPLATE


def format_documents(documents: list[Document]) -> str:
    return "\n\n".join([document.page_content for document in documents])


def format_messages(messages: Sequence[BaseMessage]) -> str:
    return "\n\n".join(
        f"{'User' if isinstance(message, HumanMessage) else 'AI'}: {message.content}"
        for message in messages
    )


def create_llm_chain(template: str, model: BaseChatModel) -> Runnable:
    return (
        ChatPromptTemplate.from_template(template)
        | model
        | StrOutputParser()
    )


def create_structured_output_llm_chain(
        schema: Type[BaseModel],
        template: str,
        model: BaseChatModel
) -> Runnable:
    parser = PydanticOutputParser(pydantic_object=schema)
    return (
        ChatPromptTemplate
        .from_messages([("system", template)])
        .partial(format_instructions=parser.get_format_instructions())
        | model
        | parser
    )


class MessagesSummarizer:
    def __init__(self, model: BaseChatModel) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.llm_chain = create_llm_chain(SUMMARIZATION_TEMPLATE, model)

    async def summarize(self, messages: Sequence[BaseMessage]) -> str:
        self.logger.debug("---SUMMARIZE MESSAGES---")
        formatted_messages = format_messages(messages)
        summary = await self.llm_chain.ainvoke({"messages": formatted_messages})
        return summary
