"""
System Monitoring Script for WhatsApp Agent Dispatch System

This script monitors the system status and job progress in real-time.
"""

import requests
import time as time_module
from datetime import datetime

BASE_URL = "https://web-production-8cec.up.railway.app"

def monitor_system():
    """Monitor the system status and job progress."""
    
    print("📊 WhatsApp Agent System Monitor")
    print("=" * 50)
    print(f"Monitoring URL: {BASE_URL}")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Monitor for 5 minutes
    for i in range(30):  # 30 iterations * 10 seconds = 5 minutes
        print(f"\n🔄 Check #{i+1} - {datetime.now().strftime('%H:%M:%S')}")
        
        # Check system health
        try:
            health_response = requests.get(f"{BASE_URL}/health", timeout=5)
            if health_response.status_code == 200:
                print("✅ System: Healthy")
            else:
                print(f"❌ System: Error {health_response.status_code}")
        except Exception as e:
            print(f"❌ System: Connection error - {str(e)}")
        
        # Check all jobs
        try:
            jobs_response = requests.get(f"{BASE_URL}/api/jobs/", timeout=5)
            if jobs_response.status_code == 200:
                jobs = jobs_response.json()
                print(f"📋 Jobs: {len(jobs)} total")
                
                # Show recent jobs
                for job in jobs[-3:]:  # Show last 3 jobs
                    job_id = job.get('id', 'Unknown')[:8] + '...'
                    status = job.get('status', 'Unknown')
                    agent = job.get('assigned_agent', 'None')
                    date = job.get('inspection_date', 'Unknown')
                    inspection_time = job.get('inspection_time', 'Unknown')
                    print(f"   - {job_id}: {status} | Agent: {agent} | {date} {inspection_time}")
            else:
                print(f"❌ Jobs: Error {jobs_response.status_code}")
        except Exception as e:
            print(f"❌ Jobs: Connection error - {str(e)}")
        
        # Check webhook status
        try:
            webhook_response = requests.get(f"{BASE_URL}/api/webhooks/twilio/status", timeout=5)
            if webhook_response.status_code == 200:
                print("✅ Webhook: Active")
            else:
                print(f"❌ Webhook: Error {webhook_response.status_code}")
        except Exception as e:
            print(f"❌ Webhook: Connection error - {str(e)}")
        
        print("-" * 40)
        
        # Wait 10 seconds before next check
        if i < 29:  # Don't wait after the last check
            time_module.sleep(10)
    
    print(f"\n🎯 Monitoring completed at {datetime.now().strftime('%H:%M:%S')}")
    print("Check Railway logs for detailed webhook activity")

def check_specific_job(job_id):
    """Check the status of a specific job."""
    
    print(f"🔍 Checking Job: {job_id}")
    print("=" * 40)
    
    try:
        job_response = requests.get(f"{BASE_URL}/api/jobs/{job_id}", timeout=5)
        
        if job_response.status_code == 200:
            job = job_response.json()
            print(f"✅ Job Status: {job.get('status', 'Unknown')}")
            print(f"   Assigned Agent: {job.get('assigned_agent', 'None')}")
            print(f"   Inspection Date: {job.get('inspection_date', 'Unknown')}")
            print(f"   Inspection Time: {job.get('inspection_time', 'Unknown')}")
            print(f"   Created: {job.get('created_at', 'Unknown')}")
            print(f"   Updated: {job.get('updated_at', 'Unknown')}")
        else:
            print(f"❌ Job not found: {job_response.status_code}")
            
    except Exception as e:
        print(f"❌ Error checking job: {str(e)}")

if __name__ == "__main__":
    # Check the specific test job first
    check_specific_job("6fd37ad6-76d6-4b82-b24b-d492fd1e80bd")
    
    # Then start monitoring
    print(f"\n" + "="*50)
    monitor_system()
