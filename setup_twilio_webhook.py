"""
Twilio Webhook Setup Script for WhatsApp Agent Dispatch System

This script helps configure and test the Twilio webhook for WhatsApp integration.
"""

import requests
import json
from datetime import datetime, timedelta

# Railway deployment URL
BASE_URL = "https://web-production-8cec.up.railway.app"

def setup_twilio_webhook():
    """Setup guide for Twilio webhook configuration."""
    
    print("🔧 Twilio Webhook Setup Guide")
    print("=" * 50)
    print(f"Your Railway URL: {BASE_URL}")
    print("=" * 50)
    
    # Step 1: Webhook URL
    webhook_url = f"{BASE_URL}/api/webhooks/twilio/whatsapp"
    print(f"\n1. 📱 Twilio Webhook URL:")
    print(f"   {webhook_url}")
    print(f"   Copy this URL to your Twilio console")
    
    # Step 2: Twilio Console Setup Instructions
    print(f"\n2. 🛠️  Twilio Console Setup:")
    print(f"   a) Go to https://console.twilio.com")
    print(f"   b) Navigate to Messaging → Settings → WhatsApp Sandbox")
    print(f"   c) Set the webhook URL to: {webhook_url}")
    print(f"   d) Save the configuration")
    
    # Step 3: Test the webhook endpoint
    print(f"\n3. 🧪 Testing webhook endpoint...")
    try:
        test_response = requests.get(f"{BASE_URL}/api/webhooks/twilio/status")
        if test_response.status_code == 200:
            print(f"   ✅ Webhook endpoint is accessible")
        else:
            print(f"   ❌ Webhook endpoint error: {test_response.status_code}")
    except Exception as e:
        print(f"   ❌ Webhook test failed: {str(e)}")
    
    # Step 4: Create a test job to trigger notifications
    print(f"\n4. 📋 Creating test job to trigger agent notifications...")
    
    inspection_time = datetime.now() + timedelta(minutes=10)
    inspection_date = inspection_time.strftime("%Y-%m-%d")
    inspection_time_str = inspection_time.strftime("%H:%M")
    
    job_data = {
        "property": {
            "property_id": "prop_webhook_test",
            "title": "Test Property for Webhook",
            "address": "456 Test Avenue, Lagos",
            "property_type": "House",
            "bedrooms": 4,
            "bathrooms": 3,
            "price": 75000000,
            "area": "200 sqm"
        },
        "client": {
            "client_id": "client_webhook_test",
            "name": "Webhook Test Client",
            "phone": "+2348034567890",
            "email": "webhook.test@email.com"
        },
        "inspection_date": inspection_date,
        "inspection_time": inspection_time_str,
        "notes": "Test job for webhook verification"
    }
    
    try:
        job_response = requests.post(
            f"{BASE_URL}/api/jobs/",
            json=job_data,
            headers={"Content-Type": "application/json"}
        )
        
        if job_response.status_code == 201:
            job_result = job_response.json()
            job_id = job_result.get("id")
            print(f"   ✅ Test job created successfully!")
            print(f"   Job ID: {job_id}")
            print(f"   Inspection: {inspection_date} at {inspection_time_str}")
            print(f"   Agents should receive WhatsApp notifications")
        else:
            print(f"   ❌ Failed to create test job: {job_response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error creating test job: {str(e)}")
    
    # Step 5: WhatsApp Testing Instructions
    print(f"\n5. 📱 WhatsApp Testing Instructions:")
    print(f"   a) Send 'YES' to your Twilio WhatsApp number")
    print(f"   b) This should assign the test job to an agent")
    print(f"   c) Send 'CONFIRM' to confirm the schedule")
    print(f"   d) Send 'START' when inspection time arrives")
    print(f"   e) Send 'COMPLETE' when inspection is done")
    
    # Step 6: Monitor logs
    print(f"\n6. 📊 Monitoring:")
    print(f"   - Check Railway logs for webhook activity")
    print(f"   - Monitor job status changes")
    print(f"   - Verify WhatsApp message delivery")
    
    print(f"\n🎯 Next Steps:")
    print(f"   1. Configure webhook URL in Twilio console")
    print(f"   2. Test with WhatsApp messages")
    print(f"   3. Monitor Railway logs")
    print(f"   4. Verify agent assignments")

def test_webhook_directly():
    """Test the webhook endpoint directly with simulated data."""
    
    print(f"\n🧪 Direct Webhook Test")
    print("=" * 30)
    
    # Simulate a WhatsApp message from agent +2347055699437
    webhook_data = {
        "From": "whatsapp:+2347055699437",
        "Body": "YES"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/webhooks/twilio/whatsapp",
            data=webhook_data
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Webhook test successful!")
            print(f"Response: {result}")
        else:
            print(f"❌ Webhook test failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Webhook test error: {str(e)}")

if __name__ == "__main__":
    setup_twilio_webhook()
    test_webhook_directly()
