from langgraph.graph import START, StateGraph
from langgraph.graph.graph import CompiledGraph
from langgraph.checkpoint.base import BaseCheckpointSaver

from ..base import BaseNode
from .state import SupervisorState
from .nodes import SupervisorAgent


def create_supervisor_agent(
        supervisor: SupervisorAgent,
        agents: list[BaseNode],
        checkpoint_saver: BaseCheckpointSaver
) -> CompiledGraph:
    workflow = StateGraph(SupervisorState)
    workflow.add_node("supervisor", supervisor)
    for agent in agents:
        workflow.add_node(agent.name, agent)
    workflow.add_edge(START, "supervisor")
    return workflow.compile(checkpointer=checkpoint_saver)
