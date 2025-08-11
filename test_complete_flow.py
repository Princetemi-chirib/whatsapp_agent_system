#!/usr/bin/env python3
"""
Test script to verify the complete inspection workflow
"""

import os
import sys
import requests
import json
from datetime import datetime, timedelta

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from services.database import db_service

def test_complete_flow():
    """Test the complete inspection workflow"""
    print("=== Complete Inspection Flow Test ===")
    
    base_url = "http://localhost:5000"
    
    # Step 1: Create a new inspection request
    print("\n1. Creating inspection request...")
    inspection_time = (datetime.now() + timedelta(minutes=5)).strftime("%H:%M")
    inspection_date = datetime.now().strftime("%Y-%m-%d")
    
    inspection_data = {
        "property": {
            "property_id": "test_flow_complete_001",
            "title": "Complete Flow Test Property",
            "address": "123 Complete Test Street, Lagos",
            "property_type": "Apartment",
            "bedrooms": 2,
            "bathrooms": 1,
            "price": 50000000,
            "area": "100 sqm"
        },
        "client": {
            "client_id": "test_client_complete_001",
            "name": "Complete Test Client",
            "phone": "+2348012345678",
            "email": "completetest@example.com"
        },
        "inspection_date": inspection_date,
        "inspection_time": inspection_time,
        "notes": "Testing complete workflow"
    }
    
    response = requests.post(
        f"{base_url}/api/jobs/",
        json=inspection_data,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 201:
        job_data = response.json()
        job_id = job_data.get('id')
        print(f"✅ Inspection created with ID: {job_id}")
        print(f"   Status: {job_data.get('status')}")
        print(f"   Assigned Agent: {job_data.get('assigned_agent')}")
    else:
        print(f"❌ Failed to create inspection: {response.status_code}")
        return
    
    # Step 2: Simulate first agent saying YES
    print("\n2. First agent (+2347055699437) says YES...")
    webhook_data = {
        "From": "whatsapp:+2347055699437",
        "Body": "YES"
    }
    
    response = requests.post(
        f"{base_url}/api/webhooks/twilio/whatsapp",
        data=webhook_data
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ First agent response: {result.get('message')}")
    else:
        print(f"❌ First agent response failed: {response.status_code}")
    
    # Step 3: Check job status after first agent
    print("\n3. Checking job status after first agent...")
    response = requests.get(f"{base_url}/api/jobs/{job_id}")
    if response.status_code == 200:
        job = response.json()
        print(f"   Status: {job.get('status')}")
        print(f"   Assigned Agent: {job.get('assigned_agent')}")
    
    # Step 4: Simulate second agent saying YES (should get different response)
    print("\n4. Second agent (+2348012345678) says YES...")
    webhook_data = {
        "From": "whatsapp:+2348012345678",
        "Body": "YES"
    }
    
    response = requests.post(
        f"{base_url}/api/webhooks/twilio/whatsapp",
        data=webhook_data
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Second agent response: {result.get('message')}")
    else:
        print(f"❌ Second agent response failed: {response.status_code}")
    
    # Step 5: First agent confirms schedule
    print("\n5. First agent confirms schedule...")
    webhook_data = {
        "From": "whatsapp:+2347055699437",
        "Body": "CONFIRM"
    }
    
    response = requests.post(
        f"{base_url}/api/webhooks/twilio/whatsapp",
        data=webhook_data
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Schedule confirmation: {result.get('message')}")
    else:
        print(f"❌ Schedule confirmation failed: {response.status_code}")
    
    # Step 6: Check final job status
    print("\n6. Final job status...")
    response = requests.get(f"{base_url}/api/jobs/{job_id}")
    if response.status_code == 200:
        job = response.json()
        print(f"   Status: {job.get('status')}")
        print(f"   Assigned Agent: {job.get('assigned_agent')}")
        print(f"   Inspection Date: {job.get('inspection_date')}")
        print(f"   Inspection Time: {job.get('inspection_time')}")
    
    # Step 7: Check database for all jobs
    print("\n7. All jobs in database:")
    jobs = db_service.find_documents('jobs', {}, limit=10)
    for job in jobs:
        print(f"   - {job.get('job_id', 'N/A')}: {job.get('status', 'N/A')} -> {job.get('assigned_agent', 'None')}")
    
    print("\n=== Test Complete ===")
    print("Next steps:")
    print("1. Wait for the reminder (1 minute before inspection time)")
    print("2. Reply 'START' when inspection time arrives")
    print("3. Reply 'COMPLETE' when inspection is finished")

if __name__ == "__main__":
    test_complete_flow()
