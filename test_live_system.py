"""
Live System Test Script for WhatsApp Agent Dispatch System

This script tests the complete flow using the live Railway deployment
with the agent +2347055699437.
"""

import requests
import json
import time
from datetime import datetime, timedelta

# Railway deployment URL
BASE_URL = "https://web-production-8cec.up.railway.app"

def test_live_system():
    """Test the complete live system flow."""
    
    print("🚀 Testing Live WhatsApp Agent System")
    print("=" * 50)
    print(f"Target URL: {BASE_URL}")
    print(f"Test Agent: +2347055699437")
    print("=" * 50)
    
    # Step 1: Check system health
    print("\n1. Checking system health...")
    try:
        health_response = requests.get(f"{BASE_URL}/health")
        if health_response.status_code == 200:
            print("✅ System is healthy")
        else:
            print(f"❌ System health check failed: {health_response.status_code}")
            return
    except Exception as e:
        print(f"❌ Health check error: {str(e)}")
        return
    
    # Step 2: Create a new inspection job
    print("\n2. Creating new inspection job...")
    
    # Set inspection time to 5 minutes from now
    inspection_time = datetime.now() + timedelta(minutes=5)
    inspection_date = inspection_time.strftime("%Y-%m-%d")
    inspection_time_str = inspection_time.strftime("%H:%M")
    
    job_data = {
        "property": {
            "property_id": "prop_test_001",
            "title": "3-Bedroom Luxury Apartment",
            "address": "123 Test Street, Lagos",
            "property_type": "Apartment",
            "bedrooms": 3,
            "bathrooms": 2,
            "price": 50000000,
            "area": "150 sqm"
        },
        "client": {
            "client_id": "client_test_001",
            "name": "Test Client",
            "phone": "+2348034567890",
            "email": "test.client@email.com"
        },
        "inspection_date": inspection_date,
        "inspection_time": inspection_time_str,
        "notes": "Test inspection for live system"
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
            print(f"✅ Job created successfully!")
            print(f"   Job ID: {job_id}")
            print(f"   Status: {job_result.get('status')}")
            print(f"   Inspection Date: {inspection_date}")
            print(f"   Inspection Time: {inspection_time_str}")
        else:
            print(f"❌ Failed to create job: {job_response.status_code}")
            print(f"Response: {job_response.text}")
            return
            
    except Exception as e:
        print(f"❌ Error creating job: {str(e)}")
        return
    
    # Step 3: Simulate agent response (YES)
    print(f"\n3. Simulating agent +2347055699437 response (YES)...")
    
    agent_response_data = {
        "agent_phone": "+2347055699437",
        "response": "YES"
    }
    
    try:
        response_response = requests.post(
            f"{BASE_URL}/api/jobs/{job_id}/agent_response",
            json=agent_response_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response_response.status_code == 200:
            response_result = response_response.json()
            print(f"✅ Agent response processed!")
            print(f"   Message: {response_result.get('message', 'No message')}")
        else:
            print(f"❌ Failed to process agent response: {response_response.status_code}")
            print(f"Response: {response_response.text}")
            
    except Exception as e:
        print(f"❌ Error processing agent response: {str(e)}")
    
    # Step 4: Check job status after agent response
    print(f"\n4. Checking job status after agent response...")
    
    try:
        status_response = requests.get(f"{BASE_URL}/api/jobs/{job_id}")
        
        if status_response.status_code == 200:
            job_status = status_response.json()
            print(f"✅ Job status retrieved!")
            print(f"   Status: {job_status.get('status')}")
            print(f"   Assigned Agent: {job_status.get('assigned_agent')}")
            print(f"   Inspection Date: {job_status.get('inspection_date')}")
            print(f"   Inspection Time: {job_status.get('inspection_time')}")
        else:
            print(f"❌ Failed to get job status: {status_response.status_code}")
            
    except Exception as e:
        print(f"❌ Error getting job status: {str(e)}")
    
    # Step 5: Simulate schedule confirmation
    print(f"\n5. Simulating schedule confirmation...")
    
    try:
        confirm_response = requests.post(f"{BASE_URL}/api/jobs/{job_id}/approve_schedule")
        
        if confirm_response.status_code == 200:
            confirm_result = confirm_response.json()
            print(f"✅ Schedule confirmed!")
            print(f"   Message: {confirm_result.get('message', 'No message')}")
        else:
            print(f"❌ Failed to confirm schedule: {confirm_response.status_code}")
            print(f"Response: {confirm_response.text}")
            
    except Exception as e:
        print(f"❌ Error confirming schedule: {str(e)}")
    
    # Step 6: Final job status check
    print(f"\n6. Final job status check...")
    
    try:
        final_response = requests.get(f"{BASE_URL}/api/jobs/{job_id}")
        
        if final_response.status_code == 200:
            final_job = final_response.json()
            print(f"✅ Final job status:")
            print(f"   Status: {final_job.get('status')}")
            print(f"   Assigned Agent: {final_job.get('assigned_agent')}")
            print(f"   Inspection Date: {final_job.get('inspection_date')}")
            print(f"   Inspection Time: {final_job.get('inspection_time')}")
        else:
            print(f"❌ Failed to get final job status: {final_response.status_code}")
            
    except Exception as e:
        print(f"❌ Error getting final job status: {str(e)}")
    
    print(f"\n🎉 Live system test completed!")
    print(f"Job ID: {job_id}")
    print(f"Test Agent: +2347055699437")
    print(f"Inspection Time: {inspection_date} at {inspection_time_str}")

if __name__ == "__main__":
    test_live_system()
