from typing import Union
from typing_extensions import TypedDict

from abc import ABC, abstractmethod

from langgraph.types import Command


class BaseNode(ABC):
    name: str

    @abstractmethod
    async def __call__(self, state: TypedDict) -> Union[dict, Command]: pass
