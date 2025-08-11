from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from app.services.job_service import JobService

router = APIRouter()

# Pydantic models for real estate inspection system
class PropertyBase(BaseModel):
    property_id: str
    title: str
    address: str
    property_type: str
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    price: Optional[float] = None
    area: Optional[str] = None

class ClientBase(BaseModel):
    client_id: str
    name: str
    phone: str
    email: Optional[str] = None

class InspectionRequest(BaseModel):
    property: PropertyBase
    client: ClientBase
    inspection_date: str
    inspection_time: str
    notes: Optional[str] = None

class AgentResponse(BaseModel):
    agent_phone: str
    response: str  # "YES" or "NO"

class JobBase(BaseModel):
    property_id: str
    client_id: str
    inspection_date: str
    inspection_time: str
    status: str = "pending"
    assigned_agent: Optional[str] = None
    notes: Optional[str] = None

class JobCreate(JobBase):
    pass

class JobUpdate(BaseModel):
    status: Optional[str] = None
    assigned_agent: Optional[str] = None
    inspection_date: Optional[str] = None
    inspection_time: Optional[str] = None
    notes: Optional[str] = None

class JobResponse(JobBase):
    id: str
    created_at: str
    updated_at: str
    property_details: Optional[PropertyBase] = None
    client_details: Optional[ClientBase] = None

    class Config:
        from_attributes = True

# Dependency injection
def get_job_service():
    return JobService()

@router.get("/", response_model=List[JobResponse])
async def get_jobs(job_service: JobService = Depends(get_job_service)):
    """Get all inspection jobs."""
    try:
        jobs = job_service.get_all_jobs()
        return jobs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: str, job_service: JobService = Depends(get_job_service)):
    """Get a specific inspection job by ID."""
    try:
        job = job_service.get_job_by_id(job_id)
        if job:
            return job
        else:
            raise HTTPException(status_code=404, detail="Inspection job not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=JobResponse, status_code=201)
async def create_inspection_request(request: InspectionRequest, job_service: JobService = Depends(get_job_service)):
    """Create a new inspection request and notify all agents."""
    try:
        job_data = {
            "property_id": request.property.property_id,
            "client_id": request.client.client_id,
            "inspection_date": request.inspection_date,
            "inspection_time": request.inspection_time,
            "notes": request.notes,
            "property_details": request.property.dict(),
            "client_details": request.client.dict()
        }
        created_job = job_service.create_inspection_request(job_data)
        return created_job
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{job_id}/agent_response")
async def handle_agent_response(job_id: str, response: AgentResponse, job_service: JobService = Depends(get_job_service)):
    """Handle agent response to inspection request."""
    try:
        result = job_service.handle_agent_response(job_id, response.agent_phone, response.response)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{job_id}", response_model=JobResponse)
async def update_job(job_id: str, job: JobUpdate, job_service: JobService = Depends(get_job_service)):
    """Update an existing inspection job."""
    try:
        job_data = job.dict(exclude_unset=True)
        updated_job = job_service.update_job(job_id, job_data)
        if updated_job:
            return updated_job
        else:
            raise HTTPException(status_code=404, detail="Inspection job not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{job_id}")
async def delete_job(job_id: str, job_service: JobService = Depends(get_job_service)):
    """Delete an inspection job."""
    try:
        success = job_service.delete_job(job_id)
        if success:
            return {"message": "Inspection job deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Inspection job not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{job_id}/approve_schedule")
async def approve_inspection_schedule(job_id: str, job_service: JobService = Depends(get_job_service)):
    """Approve inspection schedule by assigned agent."""
    try:
        result = job_service.approve_inspection_schedule(job_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{job_id}/complete_inspection")
async def complete_inspection(job_id: str, job_service: JobService = Depends(get_job_service)):
    """Mark inspection as completed."""
    try:
        result = job_service.complete_inspection(job_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/agent/{agent_phone}/jobs", response_model=List[JobResponse])
async def get_agent_jobs(agent_phone: str, job_service: JobService = Depends(get_job_service)):
    """Get all jobs assigned to a specific agent."""
    try:
        jobs = job_service.get_jobs_by_agent(agent_phone)
        return jobs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/client/{client_id}/jobs", response_model=List[JobResponse])
async def get_client_jobs(client_id: str, job_service: JobService = Depends(get_job_service)):
    """Get all jobs for a specific client."""
    try:
        jobs = job_service.get_jobs_by_client(client_id)
        return jobs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/property/{property_id}/jobs", response_model=List[JobResponse])
async def get_property_jobs(property_id: str, job_service: JobService = Depends(get_job_service)):
    """Get all jobs for a specific property."""
    try:
        jobs = job_service.get_jobs_by_property(property_id)
        return jobs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
