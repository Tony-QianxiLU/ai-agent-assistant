import streamlit as st

from ai_agent_assistant.config import settings
from ai_agent_assistant.graph import AgentGraph
from ai_agent_assistant.planner import LocalPlanner, OpenAIPlanner


st.set_page_config(page_title="AI Agent Assistant", page_icon="AI", layout="wide")

st.title("AI Agent Assistant")
st.caption("A portfolio project for LangGraph-based tool-using agents.")

with st.sidebar:
    st.header("Project Status")
    st.write("Phase 1: portfolio-ready local agent prototype.")
    planner_mode = st.radio("Planner", options=["Local deterministic", "OpenAI"])

default_task = "Calculate 24 * 7 + 13"
task = st.text_area("Task", value=default_task, height=120)

if planner_mode == "OpenAI" and settings.openai_api_key:
    planner = OpenAIPlanner(model=settings.openai_model)
elif planner_mode == "OpenAI":
    st.warning("OPENAI_API_KEY is not set. Falling back to local deterministic planner.")
    planner = LocalPlanner()
else:
    planner = LocalPlanner()

agent = AgentGraph(planner=planner)

if st.button("Run agent", type="primary"):
    result = agent.invoke(task)

    st.subheader("Plan")
    st.write(result["plan"].reasoning)

    st.subheader("Tool Calls")
    if result["plan"].tool_calls:
        for tool_call in result["plan"].tool_calls:
            st.code(f"{tool_call.name}({tool_call.arguments})")
    else:
        st.write("No tool calls.")

    st.subheader("Answer")
    st.write(result["answer"])

