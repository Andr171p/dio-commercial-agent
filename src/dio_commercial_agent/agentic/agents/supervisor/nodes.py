from typing import Literal

import logging

from pydantic import BaseModel, Field

from langchain_core.messages import AIMessage
from langchain_core.vectorstores import VectorStore
from langchain_core.language_models import BaseChatModel

from langgraph.graph import END
from langgraph.types import Command

from ..base import BaseNode
from .state import SupervisorState
from ..rag import create_rag_agent
from ..templates import (
    SUPERVISOR_TEMPLATE,
    ADVISER_TEMPLATE,
    PRICE_LIST_TEMPLATE
)
from ..utils import (
    MessagesSummarizer,
    create_structured_output_llm_chain,
    format_messages
)


SupervisorOutput = Command[Literal["consultant", "price_list"]]


class FirstStep(BaseModel):
    next_agent: str = Field(
        description="Идентификатор агента для обработки запроса: 'consultant' или 'price_list'",
        examples=["consultant", "price_list"]
    )
    final_answer: str = Field(
        description="Ответ пользователю, если запрос не требует перенаправления или нужны уточнения"
    )


class SupervisorAgent(BaseNode):
    name = "supervisor"

    def __init__(self, model: BaseChatModel) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.llm_chain = create_structured_output_llm_chain(
            schema=FirstStep,
            template=SUPERVISOR_TEMPLATE,
            model=model
        )

    async def __call__(self, state: SupervisorState) -> SupervisorOutput:
        self.logger.info("---CALL SUPERVISOR AGENT---")
        formatted_messages = format_messages(state["messages"])
        question = state["messages"][-1].content
        first_step: FirstStep = await self.llm_chain.ainvoke({
            "messages": formatted_messages,
            "question": question
        })
        print(first_step)
        if first_step.final_answer and not first_step.next_agent:
            return Command(
                update={"messages": [AIMessage(content=first_step.final_answer)]},
                goto=END
            )
        elif first_step.next_agent:
            return Command(goto=first_step.next_agent)
        else:
            return Command(
                update={"messages": [AIMessage(content="Произошла ошибка, попробуйте позже")]},
                goto=END
            )


class PriceListAgent(BaseNode):
    name = "price_list"

    def __init__(
            self,
            vector_store: VectorStore,
            model: BaseChatModel,
            top_k: int,
    ) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.messages_summarizer = MessagesSummarizer(model)
        self.rag_agent = create_rag_agent(
            vector_store=vector_store,
            top_k=top_k,
            model=model,
            template=PRICE_LIST_TEMPLATE
        )

    async def __call__(self, state: SupervisorState) -> dict[str, list[AIMessage | dict]]:
        self.logger.info("---CALL PRICE-LIST AGENT---")
        messages = state["messages"]
        last_message = messages[-1].content
        summary = await self.messages_summarizer.summarize(messages)
        last_message_with_summary = f"{summary}\n\n{last_message}"
        response = await self.rag_agent.ainvoke({"question": last_message_with_summary})
        return {"messages": [AIMessage(content=response["answer"])]}


class ConsultantAgent(BaseNode):
    name = "consultant"

    def __init__(
            self,
            vector_store: VectorStore,
            model: BaseChatModel,
            top_k: int,
    ) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.messages_summarizer = MessagesSummarizer(model)
        self.rag_agent = create_rag_agent(
            vector_store=vector_store,
            top_k=top_k,
            model=model,
            template=ADVISER_TEMPLATE
        )

    async def __call__(self, state: SupervisorState) -> dict[str, list[AIMessage | dict]]:
        self.logger.info("---CALL CONSULTANT AGENT---")
        messages = state["messages"]
        last_message = messages[-1].content
        summary = await self.messages_summarizer.summarize(messages)
        last_message_with_summary = f"{summary}\n\n{last_message}"
        response = await self.rag_agent.ainvoke({"question": last_message_with_summary})
        return {"messages": [AIMessage(content=response["answer"])]}
