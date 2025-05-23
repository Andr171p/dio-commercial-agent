from langgraph.checkpoint.base import BaseCheckpointSaver

from .agents.supervisor import create_supervisor_agent
from .agents.supervisor.nodes import SupervisorAgent, ConsultantAgent, PriceListAgent

from ..core.base import AIAgent
from ..core.entities import UserMessage, AIMessage


class OrchestratorAgent(AIAgent):
    def __init__(
            self,
            supervisor: SupervisorAgent,
            consultant: ConsultantAgent,
            price_list: PriceListAgent,
            checkpoint_saver: BaseCheckpointSaver
    ) -> None:
        self.supervisor_agent = create_supervisor_agent(
            supervisor=supervisor,
            agents=[consultant, price_list],
            checkpoint_saver=checkpoint_saver
        )

    async def generate(self, user_message: UserMessage) -> AIMessage:
        config = {"configurable": {"thread_id": user_message.chat_id}}
        inputs = {"messages": [{"role": "human", "content": user_message.text}]}
        response = await self.supervisor_agent.ainvoke(inputs, config=config)
        last_message = response["messages"][-1]
        return AIMessage(chat_id=user_message.chat_id, text=last_message.content)
