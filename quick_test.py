"""
Quick Test Script for WhatsApp Agent System

This script quickly tests the system with the new job and monitors progress.
"""

import requests
import time
from datetime import datetime

BASE_URL = "https://web-production-8cec.up.railway.app"
JOB_ID = "96ccabb3-5fe7-4865-b15e-a2fc0bd5234f"

def quick_test():
    """Quick test of the system."""
    
    print("🚀 Quick WhatsApp Agent System Test")
    print("=" * 50)
    print(f"Job ID: {JOB_ID}")
    print(f"Time: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 50)
    
    # Step 1: Check current job status
    print("\n1. 📋 Checking current job status...")
    try:
        job_response = requests.get(f"{BASE_URL}/api/jobs/{JOB_ID}", timeout=5)
        if job_response.status_code == 200:
            job = job_response.json()
            print(f"✅ Job Status: {job.get('status', 'Unknown')}")
            print(f"   Assigned Agent: {job.get('assigned_agent', 'None')}")
            print(f"   Inspection: {job.get('inspection_date')} at {job.get('inspection_time')}")
        else:
            print(f"❌ Job not found: {job_response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Step 2: Test webhook directly
    print("\n2. 🧪 Testing webhook with agent +2347055699437...")
    webhook_data = {
        "From": "whatsapp:+2347055699437",
        "Body": "YES"
    }
    
    try:
        webhook_response = requests.post(
            f"{BASE_URL}/api/webhooks/twilio/whatsapp",
            data=webhook_data,
            timeout=5
        )
        
        if webhook_response.status_code == 200:
            result = webhook_response.json()
            print(f"✅ Webhook Response: {result}")
        else:
            print(f"❌ Webhook Error: {webhook_response.status_code}")
            print(f"Response: {webhook_response.text}")
    except Exception as e:
        print(f"❌ Webhook Error: {str(e)}")
    
    # Step 3: Check job status after webhook
    print("\n3. 📋 Checking job status after webhook...")
    time.sleep(2)  # Wait a moment for processing
    
    try:
        job_response = requests.get(f"{BASE_URL}/api/jobs/{JOB_ID}", timeout=5)
        if job_response.status_code == 200:
            job = job_response.json()
            print(f"✅ Updated Job Status: {job.get('status', 'Unknown')}")
            print(f"   Assigned Agent: {job.get('assigned_agent', 'None')}")
            print(f"   Inspection: {job.get('inspection_date')} at {job.get('inspection_time')}")
        else:
            print(f"❌ Job not found: {job_response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Step 4: Test schedule confirmation
    print("\n4. ✅ Testing schedule confirmation...")
    webhook_data = {
        "From": "whatsapp:+2347055699437",
        "Body": "CONFIRM"
    }
    
    try:
        webhook_response = requests.post(
            f"{BASE_URL}/api/webhooks/twilio/whatsapp",
            data=webhook_data,
            timeout=5
        )
        
        if webhook_response.status_code == 200:
            result = webhook_response.json()
            print(f"✅ Confirmation Response: {result}")
        else:
            print(f"❌ Confirmation Error: {webhook_response.status_code}")
    except Exception as e:
        print(f"❌ Confirmation Error: {str(e)}")
    
    # Step 5: Final status check
    print("\n5. 📊 Final status check...")
    time.sleep(2)
    
    try:
        job_response = requests.get(f"{BASE_URL}/api/jobs/{JOB_ID}", timeout=5)
        if job_response.status_code == 200:
            job = job_response.json()
            print(f"✅ Final Job Status: {job.get('status', 'Unknown')}")
            print(f"   Assigned Agent: {job.get('assigned_agent', 'None')}")
            print(f"   Inspection: {job.get('inspection_date')} at {job.get('inspection_time')}")
        else:
            print(f"❌ Job not found: {job_response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print(f"\n🎯 Test completed at {datetime.now().strftime('%H:%M:%S')}")
    print("Check Railway logs for detailed activity")

if __name__ == "__main__":
    quick_test()
