from fastapi import APIRouter, HTTPException
from app.services.whatsapp_service import WhatsAppService

router = APIRouter()

@router.post("/test-twilio")
async def test_twilio():
    """Test Twilio credentials and send a test message."""
    try:
        whatsapp_service = WhatsAppService()
        
        # Check if credentials are loaded
        if not whatsapp_service.account_sid:
            raise HTTPException(status_code=500, detail="TWILIO_ACCOUNT_SID not configured")
        
        if not whatsapp_service.auth_token:
            raise HTTPException(status_code=500, detail="TWILIO_AUTH_TOKEN not configured")
        
        if not whatsapp_service.whatsapp_number:
            raise HTTPException(status_code=500, detail="TWILIO_WHATSAPP_NUMBER not configured")
        
        # Try to send a test message
        result = whatsapp_service.send_message(
            "+2347055699437",
            "🧪 Railway Twilio Test: Testing if Railway can send WhatsApp messages"
        )
        
        if result.get("success"):
            return {
                "status": "success",
                "message": "Twilio test successful",
                "message_id": result.get("message_id"),
                "credentials": {
                    "account_sid": whatsapp_service.account_sid[:10] + "...",
                    "whatsapp_number": whatsapp_service.whatsapp_number
                }
            }
        else:
            return {
                "status": "error",
                "message": "Twilio test failed",
                "error": result.get("error"),
                "credentials": {
                    "account_sid": whatsapp_service.account_sid[:10] + "..." if whatsapp_service.account_sid else None,
                    "whatsapp_number": whatsapp_service.whatsapp_number
                }
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"Test failed: {str(e)}"
        }
