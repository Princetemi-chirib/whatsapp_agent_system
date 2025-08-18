"""
Debug Job Creation

This script debugs the job creation process to see why initial notifications might not be sent.
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "https://web-production-8cec.up.railway.app"

def debug_job_creation():
    """Debug the job creation process."""
    
    print("🔍 Debugging Job Creation Process")
    print("=" * 50)
    print(f"Time: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 50)
    
    # Test 1: Check system health
    print("\n1. 🏥 Checking System Health...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✅ System is healthy")
        else:
            print(f"❌ System health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ System health error: {str(e)}")
        return
    
    # Test 2: Check debug endpoint for database connection
    print("\n2. 🔍 Checking Database Connection...")
    try:
        response = requests.get(f"{BASE_URL}/debug", timeout=10)
        if response.status_code == 200:
            debug_data = response.json()
            print("✅ Debug endpoint working")
            print(f"   Database Connected: {debug_data.get('database', {}).get('connected', False)}")
            print(f"   Database Name: {debug_data.get('database', {}).get('database_name', 'NOT_CONNECTED')}")
        else:
            print(f"❌ Debug endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Debug endpoint error: {str(e)}")
    
    # Test 3: Create a job and see what happens
    print("\n3. 🚀 Creating Test Job...")
    tomorrow = datetime.now() + timedelta(days=1)
    inspection_date = tomorrow.strftime("%Y-%m-%d")
    
    job_data = {
        "property": {
            "property_id": "debug_001",
            "title": "Debug Test Property",
            "address": "Debug Address",
            "property_type": "Apartment",
            "bedrooms": 2,
            "bathrooms": 1
        },
        "client": {
            "client_id": "debug_001",
            "name": "Debug Client",
            "phone": "+2348000000000",
            "email": "debug@test.com"
        },
        "inspection_date": inspection_date,
        "inspection_time": "15:00",
        "notes": "Debug test job"
    }
    
    try:
        print("   Sending job creation request...")
        response = requests.post(f"{BASE_URL}/api/jobs/", json=job_data, timeout=30)
        
        if response.status_code == 201:
            job_response = response.json()
            print(f"✅ Job created successfully!")
            print(f"   Job ID: {job_response.get('job_id', 'N/A')}")
            print(f"   Status: {job_response.get('status', 'N/A')}")
            print(f"   Assigned Agent: {job_response.get('assigned_agent', 'None')}")
            
            # Check if the job was created with the right data
            print(f"   Property Details: {job_response.get('property_details', 'N/A')}")
            print(f"   Client Details: {job_response.get('client_details', 'N/A')}")
            
        else:
            print(f"❌ Job creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error creating job: {str(e)}")
    
    # Test 4: Check if there are any jobs in the database
    print("\n4. 📋 Checking Jobs in Database...")
    try:
        response = requests.get(f"{BASE_URL}/api/jobs/", timeout=10)
        if response.status_code == 200:
            jobs = response.json()
            print(f"✅ Found {len(jobs)} jobs in database")
            if len(jobs) > 0:
                for i, job in enumerate(jobs[:3]):  # Show first 3 jobs
                    print(f"   Job {i+1}:")
                    print(f"     ID: {job.get('job_id', 'N/A')}")
                    print(f"     Status: {job.get('status', 'N/A')}")
                    print(f"     Assigned Agent: {job.get('assigned_agent', 'None')}")
                    print(f"     Property: {job.get('property_details', {}).get('title', 'N/A')}")
            else:
                print("   No jobs found in database")
        else:
            print(f"❌ Failed to get jobs: {response.status_code}")
    except Exception as e:
        print(f"❌ Error checking jobs: {str(e)}")
    
    print(f"\n🎯 Job creation debug completed!")
    print("Check the logs above to see what's happening during job creation.")

if __name__ == "__main__":
    debug_job_creation()




