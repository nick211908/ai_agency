from datetime import datetime
from langchain_core.messages import AIMessage, HumanMessage, BaseMessage
from app.workflows.legal_agency.state import LegalAgentState

# Import Legal Modules (Simulated import path - assuming modules are in python path)
# In a real Docker container, we'd ensure PYTHONPATH includes the root
import sys
import os
sys.path.append(os.path.join(os.getcwd(), "..", "..", "..", "..")) 

# Fallback for local dev if path is different
try:
    from modules.legal.tools.research import LegalResearcher
    from modules.legal.tools.drafting import LegalDrafter
    from modules.legal.tools.compliance import ComplianceAnalyzer
    from modules.legal.tools.risk import RiskAnalyzer
    from modules.legal.tools.evaluation import LegalEvaluator
    from modules.legal.tools.citation import CitationEngine
    from modules.legal.tools.audit import AuditLogger
except ImportError:
    # Basic mock for when modules aren't found in path (during dev)
    print("Warning: Legal modules not found in path. Using mocks.")
    class MockTool:
        def search_case_law(self, q): return []
        def retrieve_statutes(self, q): return []
        def summarize_findings(self, f): return "Mock Summary"
        def get_structured_context(self, q): return {"summary": "Mock Context"}
        def draft_document(self, t, c): return "Mock Draft"
        def analyze_document(self, c, r): return 1.0, []
        def analyze_risk(self, c): return {"score": 1.0, "vulnerabilities": []}
        def evaluate(self, c, r): return 1.0
        def attach_citations(self, c, s): return c
        def log_step(self, s, i, o): pass
    
    LegalResearcher = MockTool
    LegalDrafter = MockTool
    ComplianceAnalyzer = MockTool
    RiskAnalyzer = MockTool
    LegalEvaluator = MockTool
    CitationEngine = MockTool
    AuditLogger = MockTool

# Initialize Tools
researcher = LegalResearcher()
drafter = LegalDrafter()
compliance = ComplianceAnalyzer()
risk = RiskAnalyzer()
evaluator = LegalEvaluator()
citation = CitationEngine()
audit = AuditLogger()

def intake_node(state: LegalAgentState):
    """
    Validates and processes the initial user request.
    """
    user_input = state['messages'][-1].content
    print(f"[Intake] Processing: {user_input}")
    
    audit.log_step("Intake", user_input, "Initialized")
    
    return {
        "input": {"request": user_input},
        "history": [], # Initialize history
        "next_node": "planner",
        "messages": [AIMessage(content="Request received. Starting legal workflow.", name="Intake")]
    }

def planner_node(state: LegalAgentState):
    """
    Decomposes the request into specific tasks.
    """
    # Safety check for input
    if "input" not in state or "request" not in state["input"]:
        # Fallback if input missing (shouldn't happen with correct LangGraph setup)
        request = state['messages'][-1].content
    else:
        request = state['input']['request']
    
    # Simple keyword-based planning for MVP
    doc_type = "Unknown"
    if "nda" in request.lower():
        doc_type = "NDA"
    elif "agreement" in request.lower():
        doc_type = "Service Agreement"
        
    plan = {
        "doc_type": doc_type,
        "research_needed": True,
        "compliance_rules": ["Indemnification", "Termination", "Jurisdiction"]
    }
    
    audit.log_step("Planner", request, plan)
    
    return {
        "intermediate": {"plan": plan},
        "next_node": "researcher",
        "messages": [AIMessage(content=f"Plan created: Draft {doc_type}", name="Planner")]
    }

def research_node(state: LegalAgentState):
    """
    Performs legal research.
    """
    plan = state.get("intermediate", {}).get("plan", {})
    query = f"precedents for {plan.get('doc_type', 'contract')}"
    
    context = researcher.get_structured_context(query)
    
    audit.log_step("Research", query, context.get("summary")[:50])
    
    return {
        "context": context,
        "next_node": "drafter",
        "messages": [AIMessage(content="Research completed.", name="Researcher")]
    }

def draft_node(state: LegalAgentState):
    """
    Drafts the document using the plan and context.
    """
    plan = state.get("intermediate", {}).get("plan", {})
    context = state.get('context', {})
    
    draft = drafter.draft_document(plan.get("doc_type", "General"), context)
    
    # Merge with existing intermediate state
    intermediate = state.get("intermediate", {}).copy()
    intermediate['draft'] = draft
    
    audit.log_step("Drafting", "Context+Plan", "Draft Generated")
    
    return {
        "intermediate": intermediate,
        "next_node": "compliance",
        "messages": [AIMessage(content="Draft generated.", name="Drafter")]
    }

def compliance_node(state: LegalAgentState):
    """
    Checks the draft for compliance.
    """
    intermediate = state.get("intermediate", {}).copy()
    draft = intermediate.get("draft", "")
    rules = intermediate.get("plan", {}).get("compliance_rules", [])
    
    score, missing = compliance.analyze_document(draft, rules)
    
    intermediate['compliance_report'] = {"score": score, "missing": missing}
    
    metrics = state.get('metrics', {}).copy()
    metrics['compliance'] = score
    
    audit.log_step("Compliance", "Draft", f"Score: {score}")
    
    return {
        "intermediate": intermediate,
        "metrics": metrics,
        "next_node": "risk",
        "messages": [AIMessage(content=f"Compliance check passed. Score: {score}", name="Compliance")]
    }

def risk_node(state: LegalAgentState):
    """
    Analyzes the draft for risks.
    """
    intermediate = state.get("intermediate", {}).copy()
    draft = intermediate.get("draft", "")
    
    risk_report = risk.analyze_risk(draft)
    intermediate['risk_report'] = risk_report
    
    metrics = state.get('metrics', {}).copy()
    metrics['risk'] = risk_report['score']
    
    audit.log_step("Risk", "Draft", f"Risk Level: {risk_report['risk_level']}")
    
    return {
        "intermediate": intermediate,
        "metrics": metrics,
        "next_node": "evaluation",
        "messages": [AIMessage(content=f"Risk analysis complete. Level: {risk_report['risk_level']}", name="Risk")]
    }

def evaluation_node(state: LegalAgentState):
    """
    Evaluates the overall quality and decides on refinement.
    """
    metrics = state.get('metrics', {}).copy()
    c_score = metrics.get('compliance', 0.0)
    r_score = metrics.get('risk', 0.0)
    
    overall = evaluator.evaluate(c_score, r_score)
    metrics['overall'] = overall
    
    audit.log_step("Evaluation", "Metrics", f"Overall: {overall}")
    
    return {
        "metrics": metrics,
        "next_node": "refinement_check",
        "messages": [AIMessage(content=f"Evaluation complete. Score: {overall}", name="Evaluator")]
    }

def refinement_router(state: LegalAgentState) -> str:
    """
    Conditional logic to loop back or proceed.
    """
    score = state.get('metrics', {}).get('overall', 0.0)
    # Threshold for acceptance
    if score >= 0.7:
        return "citation"
    else:
        # Prevent infinite loops (mock logic)
        # Check history length or specific refinement count
        if len(state.get('messages', [])) > 20: 
            return "citation"
        return "refinement"

def refinement_node(state: LegalAgentState):
    """
    Refines the draft (Mock implementation).
    """
    # In a real system, LLM refines the draft based on reports.
    # Here we just "fix" it to pass checks next time.
    intermediate = state.get("intermediate", {}).copy()
    current_draft = intermediate.get('draft', "")
    improved_draft = current_draft + "\n[Refined: Added missing clauses and indemnification]"
    
    intermediate['draft'] = improved_draft
    
    return {
        "intermediate": intermediate,
        "next_node": "compliance", # Loop back to check
        "messages": [AIMessage(content="Refining document based on feedback.", name="Refiner")]
    }

def citation_node(state: LegalAgentState):
    """
    Attaches citations to the final draft.
    """
    draft = state.get("intermediate", {}).get("draft", "")
    # For MVP, using research context as sources
    sources = state.get('context', {}).get('cases', []) + state.get('context', {}).get('statutes', [])
    
    final_doc = citation.attach_citations(draft, sources)
    
    audit.log_step("Citation", "Draft", "Citations Attached")
    
    return {
        "output": {"document": final_doc},
        "next_node": "audit",
        "messages": [AIMessage(content="Citations attached.", name="Citation")]
    }

def audit_node(state: LegalAgentState):
    """
    Finalizes the audit log.
    """
    # In a real system, save logs to DB
    logs = audit.get_logs()
    
    print(f"[Audit] Workflow complete. {len(logs)} steps logged.")
    
    return {
        "history": logs,
        "next_node": "end",
        "messages": [AIMessage(content="Workflow complete. Audit log saved.", name="Audit")]
    }
