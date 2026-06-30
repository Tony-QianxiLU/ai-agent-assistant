from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph

from ai_agent_assistant.planner import LocalPlanner, Plan
from ai_agent_assistant.tools import ToolRegistry, ToolResult, default_registry


class AgentState(TypedDict, total=False):
    task: str
    plan: Plan
    tool_results: list[ToolResult]
    answer: str


class AgentGraph:
    def __init__(
        self,
        planner: Any | None = None,
        registry: ToolRegistry | None = None,
    ) -> None:
        self._planner = planner or LocalPlanner()
        self._registry = registry or default_registry()
        self._graph = self._build_graph()

    def invoke(self, task: str) -> AgentState:
        return self._graph.invoke({"task": task})

    def _build_graph(self):
        graph = StateGraph(AgentState)
        graph.add_node("plan", self._plan)
        graph.add_node("act", self._act)
        graph.add_node("respond", self._respond)
        graph.add_edge(START, "plan")
        graph.add_edge("plan", "act")
        graph.add_edge("act", "respond")
        graph.add_edge("respond", END)
        return graph.compile()

    def _plan(self, state: AgentState) -> AgentState:
        return {"plan": self._planner.plan(state["task"])}

    def _act(self, state: AgentState) -> AgentState:
        plan = state["plan"]
        results = [self._registry.run(call) for call in plan.tool_calls]
        return {"tool_results": results}

    def _respond(self, state: AgentState) -> AgentState:
        plan = state["plan"]
        results = state.get("tool_results", [])

        if not results:
            answer = (
                "I did not need to call a tool. "
                "Try a calculation, summarization, or todo extraction task."
            )
        else:
            rendered_results = "\n".join(f"{result.name}: {result.output}" for result in results)
            answer = f"Plan: {plan.reasoning}\n\nTool results:\n{rendered_results}"

        return {"answer": answer}

