"""
Test WhatsApp Flow

This script tests the complete WhatsApp integration flow.
"""

import requests
import json
from datetime import datetime

BASE_URL = "https://web-production-8cec.up.railway.app"

def test_whatsapp_flow():
    """Test the complete WhatsApp integration flow."""
    
    print("📱 Testing WhatsApp Integration Flow")
    print("=" * 50)
    print(f"Time: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 50)
    
    # Test 1: System Health
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
    
    # Test 2: Check if there are any pending jobs
    print("\n2. 📋 Checking for pending jobs...")
    try:
        response = requests.get(f"{BASE_URL}/api/jobs/", timeout=10)
        if response.status_code == 200:
            jobs = response.json()
            print(f"✅ Found {len(jobs)} jobs in database")
            if len(jobs) > 0:
                for job in jobs:
                    print(f"   - Job ID: {job.get('job_id', 'N/A')}")
                    print(f"     Status: {job.get('status', 'N/A')}")
                    print(f"     Assigned Agent: {job.get('assigned_agent', 'None')}")
                    print(f"     Location: {job.get('location', 'N/A')}")
            else:
                print("   No jobs found - creating a test job...")
                # Create a simple test job
                test_job = {
                    "property": {"property_id": "test_001", "title": "Test Property"},
                    "client": {"client_id": "test_001", "name": "Test Client"},
                    "inspection_date": "2025-08-13",
                    "inspection_time": "15:00",
                    "location": "Test Location"
                }
                job_response = requests.post(f"{BASE_URL}/api/jobs/", json=test_job, timeout=15)
                if job_response.status_code == 201:
                    print("✅ Test job created successfully")
                else:
                    print(f"❌ Failed to create test job: {job_response.status_code}")
        else:
            print(f"❌ Failed to get jobs: {response.status_code}")
    except Exception as e:
        print(f"❌ Error checking jobs: {str(e)}")
    
    # Test 3: Test Agent Response - YES
    print("\n3. 📱 Testing Agent Response: YES...")
    webhook_data = {
        "From": "whatsapp:+2347055699437",
        "Body": "YES"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/webhooks/twilio/whatsapp", data=webhook_data, timeout=10)
        if response.status_code == 200:
            webhook_response = response.json()
            print(f"✅ Webhook response: {webhook_response}")
            
            if webhook_response.get('status') == 'success':
                print("🎉 Job assigned successfully!")
            elif webhook_response.get('status') == 'no_jobs':
                print("⚠️ No pending jobs available")
            else:
                print(f"ℹ️ Response: {webhook_response.get('message', 'Unknown response')}")
        else:
            print(f"❌ Webhook error: {response.status_code}")
    except Exception as e:
        print(f"❌ Webhook error: {str(e)}")
    
    # Test 4: Test Agent Response - CONFIRM
    print("\n4. ✅ Testing Agent Response: CONFIRM...")
    webhook_data = {
        "From": "whatsapp:+2347055699437",
        "Body": "CONFIRM"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/webhooks/twilio/whatsapp", data=webhook_data, timeout=10)
        if response.status_code == 200:
            webhook_response = response.json()
            print(f"✅ Confirmation response: {webhook_response}")
            
            if webhook_response.get('status') == 'success':
                print("🎉 Schedule confirmed successfully!")
            else:
                print(f"ℹ️ Response: {webhook_response.get('message', 'Unknown response')}")
        else:
            print(f"❌ Confirmation error: {response.status_code}")
    except Exception as e:
        print(f"❌ Confirmation error: {str(e)}")
    
    print(f"\n🎯 WhatsApp integration test completed!")
    print("Check your Twilio console for message delivery status.")

if __name__ == "__main__":
    test_whatsapp_flow()





