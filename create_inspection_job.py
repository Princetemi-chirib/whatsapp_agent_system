"""
Create Inspection Job

This script creates a proper inspection job for testing the WhatsApp integration.
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "https://web-production-8cec.up.railway.app"

def create_inspection_job():
    """Create a proper inspection job."""
    
    print("🏠 Creating Inspection Job")
    print("=" * 40)
    print(f"Time: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 40)
    
    # Create inspection job data
    tomorrow = datetime.now() + timedelta(days=1)
    inspection_date = tomorrow.strftime("%Y-%m-%d")
    
    job_data = {
        "property": {
            "property_id": "prop_001",
            "title": "3-Bedroom Apartment in Lekki",
            "address": "123 Lekki Phase 1, Lagos",
            "property_type": "Apartment",
            "bedrooms": 3,
            "bathrooms": 2,
            "price": 50000000,
            "area": "150 sqm"
        },
        "client": {
            "client_id": "client_001",
            "name": "Michael Brown",
            "phone": "+2348034567890",
            "email": "michael.brown@email.com"
        },
        "inspection_type": "pre_purchase",
        "inspection_date": inspection_date,
        "inspection_time": "14:00",
        "location": "123 Lekki Phase 1, Lagos",
        "notes": "Pre-purchase inspection for 3-bedroom apartment"
    }
    
    try:
        print("\n📋 Creating inspection job...")
        response = requests.post(f"{BASE_URL}/api/jobs/", json=job_data, timeout=30)
        
        if response.status_code == 201:
            job_response = response.json()
            job_id = job_response.get("job_id")
            print(f"✅ Job created successfully!")
            print(f"   Job ID: {job_id}")
            print(f"   Status: {job_response.get('status')}")
            print(f"   Assigned Agent: {job_response.get('assigned_agent')}")
            print(f"   Inspection Date: {inspection_date}")
            print(f"   Inspection Time: 14:00")
            print(f"   Location: {job_data['location']}")
            
            if job_id:
                return job_id
            else:
                print("⚠️ Job created but no job_id returned")
                return "job_created"
        else:
            print(f"❌ Job creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error creating job: {str(e)}")
        return None

if __name__ == "__main__":
    job_id = create_inspection_job()
    if job_id:
        print(f"\n🎯 Inspection job created with ID: {job_id}")
        print("The agent should receive a WhatsApp notification shortly.")
    else:
        print("\n❌ Failed to create inspection job.")
