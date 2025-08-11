from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.jobs import router as jobs_router
from app.routes.webhooks import router as webhooks_router

app = FastAPI(
    title="WhatsApp Agent Dispatch & Inspection Notification System",
    description="A FastAPI-based system for managing real estate inspection jobs with WhatsApp integration via Twilio",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(jobs_router, prefix="/api/jobs", tags=["jobs"])
app.include_router(webhooks_router, prefix="/api/webhooks", tags=["webhooks"])

@app.get("/")
async def root():
    return {"message": "WhatsApp Agent Dispatch & Inspection Notification System API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
