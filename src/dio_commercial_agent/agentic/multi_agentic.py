from langgraph.checkpoint.base import BaseCheckpointSaver

from .agents.supervisor import create_supervisor_agent
from .agents.supervisor.nodes import SupervisorAgent, ConsultantAgent, PriceListAgent

from ..base import AIAgent


class CommercialAgent(AIAgent):
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

    async def generate(self, chat_id: str, text: str) -> str:
        config = {"configurable": {"thread_id": chat_id}}
        inputs = {"messages": [{"role": "human", "content": text}]}
        response = await self.supervisor_agent.ainvoke(inputs, config=config)
        last_message = response["messages"][-1]
        return last_message.content
