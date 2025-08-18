from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.jobs import router as jobs_router
from app.routes.webhooks import router as webhooks_router
from app.services.scheduler import scheduler_service
import os

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

# Initialize scheduler service
scheduler_service.start()

@app.get("/")
async def root():
    return {"message": "WhatsApp Agent Dispatch & Inspection Notification System API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "System is running"}

@app.get("/debug")
async def debug_info():
    """Debug endpoint to check environment variables and database connection."""
    try:
        from app.services.database import db_service
        
        # Check environment variables
        mongo_uri = os.getenv("MONGODB_URI", "NOT_SET")
        mongo_db_name = os.getenv("MONGODB_DB_NAME", "NOT_SET")
        twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID", "NOT_SET")
        twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN", "NOT_SET")
        twilio_whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER", "NOT_SET")
        
        # Check database connection
        db_connected = db_service.db is not None
        db_name = db_service.db.name if db_service.db is not None else "NOT_CONNECTED"
        
        # Test database operations (only if connected)
        test_insert = "NOT_TESTED"
        test_find = "NOT_TESTED"
        if db_service.db is not None:
            try:
                test_doc = {"test": "debug", "timestamp": "2025-08-11"}
                insert_result = db_service.insert_document("debug_test", test_doc)
                find_result = db_service.find_documents("debug_test", {"test": "debug"})
                test_insert = "SUCCESS" if insert_result else "FAILED"
                test_find = f"FOUND {len(find_result)} DOCUMENTS"
            except Exception as db_error:
                test_insert = f"ERROR: {str(db_error)}"
                test_find = "ERROR"
        
        return {
            "environment": {
                "MONGODB_URI": mongo_uri[:20] + "..." if len(mongo_uri) > 20 else mongo_uri,
                "MONGODB_DB_NAME": mongo_db_name,
                "TWILIO_ACCOUNT_SID": twilio_account_sid[:10] + "..." if len(twilio_account_sid) > 10 else twilio_account_sid,
                "TWILIO_AUTH_TOKEN": "SET" if twilio_auth_token != "NOT_SET" else "NOT_SET",
                "TWILIO_WHATSAPP_NUMBER": twilio_whatsapp_number
            },
            "database": {
                "connected": db_connected,
                "database_name": db_name,
                "test_insert": test_insert,
                "test_find": test_find
            }
        }
    except Exception as e:
        return {
            "error": str(e),
            "environment": {
                "MONGODB_URI": os.getenv("MONGODB_URI", "NOT_SET"),
                "MONGODB_DB_NAME": os.getenv("MONGODB_DB_NAME", "NOT_SET")
            }
        }

@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event to stop the scheduler."""
    scheduler_service.stop()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
