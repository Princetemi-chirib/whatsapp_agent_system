#!/usr/bin/env python3
"""
Test script to check scheduler functionality
"""

import os
import sys
from datetime import datetime, timezone

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from services.scheduler import scheduler_service
from services.database import db_service

def test_scheduler():
    """Test the scheduler functionality"""
    print("=== Scheduler Test ===")
    
    # Check if scheduler is running
    print(f"Scheduler running: {scheduler_service.scheduler.running}")
    
    # Get all scheduled jobs
    jobs = scheduler_service.get_scheduled_jobs()
    print(f"\nScheduled jobs: {len(jobs)}")
    
    for job in jobs:
        print(f"  - Job ID: {job.id}")
        print(f"    Function: {job.func.__name__}")
        print(f"    Next run: {job.next_run_time}")
        print(f"    Trigger: {job.trigger}")
        print()
    
    # Check recent jobs in database
    print("=== Recent Jobs in Database ===")
    recent_jobs = db_service.find_documents('jobs', {}, limit=5)
    
    for job in recent_jobs:
        print(f"Job ID: {job.get('job_id', 'N/A')}")
        print(f"Status: {job.get('status', 'N/A')}")
        print(f"Assigned Agent: {job.get('assigned_agent', 'N/A')}")
        print(f"Inspection Date: {job.get('inspection_date', 'N/A')}")
        print(f"Inspection Time: {job.get('inspection_time', 'N/A')}")
        print(f"Created: {job.get('created_at', 'N/A')}")
        print()

if __name__ == "__main__":
    test_scheduler()
