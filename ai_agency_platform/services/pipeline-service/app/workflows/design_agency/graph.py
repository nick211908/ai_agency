from langgraph.graph import StateGraph, START, END
from app.workflows.design_agency.state import DesignAgentState
from app.workflows.design_agency.nodes import (
    intake_node,
    designer_node,
    copywriter_node,
    review_node
)

# Define the graph
workflow = StateGraph(DesignAgentState)

# Add nodes
workflow.add_node("intake", intake_node)
workflow.add_node("designer", designer_node)
workflow.add_node("copywriter", copywriter_node)
workflow.add_node("review", review_node)

# Add edges
workflow.add_edge(START, "intake")
workflow.add_edge("intake", "designer")
workflow.add_edge("designer", "copywriter")
workflow.add_edge("copywriter", "review")
workflow.add_edge("review", END)

# Compile
design_graph = workflow.compile()
