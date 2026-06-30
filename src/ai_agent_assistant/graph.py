from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from ai_agent_assistant.memory import MemoryEntry
from ai_agent_assistant.planner import LocalPlanner, Plan, Planner
from ai_agent_assistant.tools import ToolRegistry, ToolResult, default_registry


class AgentState(TypedDict, total=False):
    task: str
    plan: Plan
    tool_results: list[ToolResult]
    memory: list[MemoryEntry]
    answer: str


class AgentGraph:
    def __init__(
        self,
        planner: Planner | None = None,
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
        graph.add_node("remember", self._remember)
        graph.add_node("respond", self._respond)
        graph.add_edge(START, "plan")
        graph.add_edge("plan", "act")
        graph.add_edge("act", "remember")
        graph.add_edge("remember", "respond")
        graph.add_edge("respond", END)
        return graph.compile()

    def _plan(self, state: AgentState) -> AgentState:
        return {"plan": self._planner.plan(state["task"])}

    def _act(self, state: AgentState) -> AgentState:
        plan = state["plan"]
        results = [self._registry.run(call) for call in plan.tool_calls]
        return {"tool_results": results}

    def _remember(self, state: AgentState) -> AgentState:
        plan = state["plan"]
        results = state.get("tool_results", [])
        memory = [
            MemoryEntry(step="task", content=state["task"]),
            MemoryEntry(step="plan", content=plan.reasoning),
        ]
        memory.extend(
            MemoryEntry(
                step=f"tool:{result.name}",
                content=f"{'success' if result.success else 'failed'} - {result.output}",
            )
            for result in results
        )
        return {"memory": memory}

    def _respond(self, state: AgentState) -> AgentState:
        plan = state["plan"]
        results = state.get("tool_results", [])

        if not results:
            answer = (
                "I did not need to call a tool. "
                "Try a calculation, summarization, or todo extraction task."
            )
        else:
            rendered_results = "\n".join(
                f"{result.name} ({'ok' if result.success else 'error'}): {result.output}"
                for result in results
            )
            answer = f"Plan: {plan.reasoning}\n\nTool results:\n{rendered_results}"

        return {"answer": answer}
