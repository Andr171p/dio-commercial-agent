from typing import Annotated, Sequence
from typing_extensions import TypedDict

from langchain_core.messages import BaseMessage

from langgraph.graph import add_messages


class SupervisorState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
