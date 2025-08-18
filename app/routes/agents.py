from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timezone
import sys
import os

# Add the services directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'services'))

from app.services.database import db_service

router = APIRouter()

class AgentBase(BaseModel):
    agent_id: str
    name: str
    phone: str
    email: str
    status: str = "active"
    zone: Optional[str] = None
    specializations: Optional[List[str]] = None
    experience_years: Optional[int] = None
    rating: Optional[float] = None
    total_inspections: Optional[int] = None

class AgentCreate(AgentBase):
    pass

class AgentResponse(AgentBase):
    id: str
    created_at: str
    updated_at: str

@router.post("/", response_model=AgentResponse)
async def create_agent(agent: AgentCreate):
    """Create a new agent."""
    try:
        agent_data = agent.dict()
        agent_data["created_at"] = datetime.now(timezone.utc).isoformat()
        agent_data["updated_at"] = datetime.now(timezone.utc).isoformat()
        
        result = db_service.insert_document("agents", agent_data)
        if result:
            agent_data["id"] = result
            return agent_data
        else:
            raise HTTPException(status_code=500, detail="Failed to create agent")
    except Exception as e:
        print(f"Error in create_agent: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[AgentResponse])
async def get_agents():
    """Get all agents."""
    try:
        agents = db_service.find_documents("agents", {})
        # Ensure each agent has the required 'id' field and handle missing fields
        processed_agents = []
        for agent in agents:
            processed_agent = {
                "agent_id": agent.get("agent_id", ""),
                "name": agent.get("name", ""),
                "phone": agent.get("phone", ""),
                "email": agent.get("email", ""),
                "status": agent.get("status", "active"),
                "zone": agent.get("zone"),
                "specializations": agent.get("specializations", []),
                "experience_years": agent.get("experience_years"),
                "rating": agent.get("rating"),
                "total_inspections": agent.get("total_inspections"),
                "id": str(agent.get("_id", "")),
                "created_at": agent.get("created_at", ""),
                "updated_at": agent.get("updated_at", "")
            }
            processed_agents.append(processed_agent)
        return processed_agents
    except Exception as e:
        print(f"Error in get_agents: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: str):
    """Get agent by ID."""
    try:
        agent = db_service.find_document_by_id("agents", agent_id)
        if agent:
            return agent
        else:
            raise HTTPException(status_code=404, detail="Agent not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
