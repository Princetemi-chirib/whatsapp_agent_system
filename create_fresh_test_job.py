"""
Create Fresh Test Job Script

This script creates a new test job that will trigger WhatsApp notifications to agents.
"""

import requests
from datetime import datetime, timedelta

BASE_URL = "https://web-production-8cec.up.railway.app"

def create_fresh_test_job():
    """Create a fresh test job to trigger agent notifications."""
    
    print("🚀 Creating Fresh Test Job")
    print("=" * 40)
    
    # Set inspection time to 15 minutes from now
    inspection_time = datetime.now() + timedelta(minutes=15)
    inspection_date = inspection_time.strftime("%Y-%m-%d")
    inspection_time_str = inspection_time.strftime("%H:%M")
    
    job_data = {
        "property": {
            "property_id": "prop_fresh_test",
            "title": "Fresh Test Property - 4 Bedroom Villa",
            "address": "789 Fresh Test Road, Victoria Island, Lagos",
            "property_type": "Villa",
            "bedrooms": 4,
            "bathrooms": 4,
            "price": 120000000,
            "area": "300 sqm"
        },
        "client": {
            "client_id": "client_fresh_test",
            "name": "Fresh Test Client",
            "phone": "+2348034567890",
            "email": "fresh.test@email.com"
        },
        "inspection_date": inspection_date,
        "inspection_time": inspection_time_str,
        "notes": "Fresh test job for WhatsApp notifications - agents should receive messages"
    }
    
    try:
        print(f"Creating job for inspection on {inspection_date} at {inspection_time_str}...")
        
        job_response = requests.post(
            f"{BASE_URL}/api/jobs/",
            json=job_data,
            headers={"Content-Type": "application/json"}
        )
        
        if job_response.status_code == 201:
            job_result = job_response.json()
            job_id = job_result.get("id")
            print(f"✅ Fresh test job created successfully!")
            print(f"   Job ID: {job_id}")
            print(f"   Status: {job_result.get('status')}")
            print(f"   Inspection: {inspection_date} at {inspection_time_str}")
            print(f"   Property: {job_data['property']['title']}")
            print(f"   Client: {job_data['client']['name']}")
            
            print(f"\n📱 WhatsApp Testing:")
            print(f"   - Agents should receive WhatsApp notifications")
            print(f"   - Send 'YES' to accept the job")
            print(f"   - Send 'CONFIRM' to confirm schedule")
            print(f"   - Send 'START' at {inspection_time_str}")
            print(f"   - Send 'COMPLETE' when done")
            
            return job_id
        else:
            print(f"❌ Failed to create job: {job_response.status_code}")
            print(f"Response: {job_response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error creating job: {str(e)}")
        return None

if __name__ == "__main__":
    create_fresh_test_job()
