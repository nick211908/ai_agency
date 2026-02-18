from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import os
import shutil

# Add modules path for imports
import sys
sys.path.append(os.path.join(os.getcwd(), "..", "..", ".."))

from app.core.graph import app_graph
from app.workflows.legal_agency.graph import legal_graph
from app.workflows.design_agency.graph import design_graph
from modules.legal.knowledge.ingestion import DocumentParser
from modules.legal.knowledge.vector_store import VectorStore
from langchain_core.messages import HumanMessage

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Agency Pipeline Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AgencyRequest(BaseModel):
    prompt: str
    agency_type: str = Field("design", description="Type of agency to run: 'design' or 'legal'")

@app.post("/run-agency")
async def run_agency(request: AgencyRequest):
    try:
        if request.agency_type == "legal":
            initial_state = {
                "messages": [HumanMessage(content=request.prompt)],
                "history": []
            }
            result = await legal_graph.ainvoke(initial_state)
            
            # Extract structured output for Legal Agency
            return {
                "status": "success",
                "agency": "legal",
                "output": result.get("output", {}),
                "metrics": result.get("metrics", {}),
                "history": result.get("history", []),
                "messages": [m.content for m in result['messages']]
            }
        elif request.agency_type == "design":
            initial_state = {
                "input": {"request": request.prompt},
                "messages": [HumanMessage(content=request.prompt)],
                "artifacts": {},
                "review": {},
                "next_node": "intake"
            }
            result = await design_graph.ainvoke(initial_state)
            return {"status": "success", "output": result}
        else:
            # Fallback (legacy)
            initial_state = {"messages": [HumanMessage(content=request.prompt)]}
            result = await app_graph.ainvoke(initial_state)
            return {"status": "success", "output": result}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    try:
        # Save uploaded file temporarily
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
            
        # Parse document
        parser = DocumentParser()
        chunks = parser.parse_file(temp_path)
        
        # Add to Vector Store
        store = VectorStore()
        store.add_documents(chunks, metadatas=[{"source": file.filename, "type": "document"} for _ in chunks])
        
        # Clean up
        os.remove(temp_path)
        
        return {"status": "success", "chunks_added": len(chunks), "filename": file.filename}
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok"}
