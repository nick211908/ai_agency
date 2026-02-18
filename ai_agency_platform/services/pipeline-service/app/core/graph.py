from langgraph.graph import StateGraph, START, END
from app.core.state import AgentState
from app.core.nodes import (
    project_manager_node,
    designer_node,
    copywriter_node,
    creative_director_node
)

# Define the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("project_manager", project_manager_node)
workflow.add_node("designer", designer_node)
workflow.add_node("copywriter", copywriter_node)
workflow.add_node("creative_director", creative_director_node)

# Add edges (Sequential flow for MVP)
workflow.add_edge(START, "project_manager")
workflow.add_edge("project_manager", "designer")
workflow.add_edge("designer", "copywriter")
workflow.add_edge("copywriter", "creative_director")
workflow.add_edge("creative_director", END)

# Compile the graph
app_graph = workflow.compile()
