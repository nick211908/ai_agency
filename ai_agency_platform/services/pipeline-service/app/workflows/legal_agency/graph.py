from langgraph.graph import StateGraph, START, END
from app.workflows.legal_agency.state import LegalAgentState
from app.workflows.legal_agency.nodes import (
    intake_node,
    planner_node,
    research_node,
    draft_node,
    compliance_node,
    risk_node,
    evaluation_node,
    refinement_node,
    citation_node,
    audit_node,
    refinement_router
)

# Define the graph
legal_workflow = StateGraph(LegalAgentState)

# Add nodes
legal_workflow.add_node("intake", intake_node)
legal_workflow.add_node("planner", planner_node)
legal_workflow.add_node("researcher", research_node)
legal_workflow.add_node("drafter", draft_node)
legal_workflow.add_node("compliance", compliance_node)
legal_workflow.add_node("risk", risk_node)
legal_workflow.add_node("evaluation", evaluation_node)
legal_workflow.add_node("refinement", refinement_node)
legal_workflow.add_node("citation", citation_node)
legal_workflow.add_node("audit", audit_node)

# Add edges
legal_workflow.add_edge(START, "intake")
legal_workflow.add_edge("intake", "planner")
legal_workflow.add_edge("planner", "researcher")
legal_workflow.add_edge("researcher", "drafter")
legal_workflow.add_edge("drafter", "compliance")
legal_workflow.add_edge("compliance", "risk")
legal_workflow.add_edge("risk", "evaluation")

# Conditional Loop
legal_workflow.add_conditional_edges(
    "evaluation",
    refinement_router,
    {
        "refinement": "refinement",
        "citation": "citation"
    }
)

legal_workflow.add_edge("refinement", "compliance") # Loop back
legal_workflow.add_edge("citation", "audit")
legal_workflow.add_edge("audit", END)

# Compile the graph
legal_graph = legal_workflow.compile()
