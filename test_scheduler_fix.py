#!/usr/bin/env python3
"""
Test Scheduler Fix
"""

import os
import sys
from datetime import datetime, timezone, timedelta

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_scheduler_initialization():
    """Test if the scheduler is properly initialized."""
    
    try:
        # Import the scheduler service
        from app.services.scheduler import scheduler_service
        
        print("✅ Scheduler service imported successfully")
        
        # Check if scheduler is running
        if scheduler_service.scheduler.running:
            print("✅ Scheduler is running")
        else:
            print("❌ Scheduler is not running")
            scheduler_service.start()
            print("✅ Scheduler started")
        
        # Test scheduling a job
        test_data = {
            'id': 'test_job_001',
            'inspection_date': datetime.now().strftime('%Y-%m-%d'),
            'inspection_time': (datetime.now() + timedelta(minutes=1)).strftime('%H:%M'),
            'assigned_agent': '+2347055699437'
        }
        
        # Schedule reminder
        reminder_result = scheduler_service.schedule_inspection_reminder(test_data)
        print(f"Reminder scheduling: {'✅ Success' if reminder_result else '❌ Failed'}")
        
        # Schedule start prompt
        start_result = scheduler_service.schedule_inspection_start_prompt(test_data)
        print(f"Start prompt scheduling: {'✅ Success' if start_result else '❌ Failed'}")
        
        # List scheduled jobs
        jobs = scheduler_service.scheduler.get_jobs()
        print(f"📋 Scheduled jobs: {len(jobs)}")
        for job in jobs:
            print(f"   - {job.id}: {job.next_run_time}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing scheduler: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing scheduler fix...")
    test_scheduler_initialization()
