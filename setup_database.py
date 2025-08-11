
"""
Database Setup Script for WhatsApp Agent Dispatch & Inspection Notification System

This script initializes the MongoDB database with all necessary collections,
indexes, and sample data for the live website integration.
"""

import os
from datetime import datetime, timezone
from app.services.database import db_service

def setup_database():
    """Initialize the database with all collections and indexes."""
    
    print("Setting up database for WhatsApp Agent Dispatch System...")
    
    # 1. AGENTS COLLECTION
    print("Creating agents collection...")
    db_service.create_index("agents", "phone", unique=True)
    db_service.create_index("agents", "email", unique=True)
    db_service.create_index("agents", "status")
    db_service.create_index("agents", "zone")
    
    # Sample agents data
    sample_agents = [
        {
            "agent_id": "agent_001",
            "name": "John Smith",
            "phone": "+2348012345678",
            "email": "john.smith@realestate.com",
            "status": "active",
            "zone": "Lekki",
            "specializations": ["Apartments", "Houses"],
            "experience_years": 5,
            "rating": 4.8,
            "total_inspections": 150,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        },
        {
            "agent_id": "agent_002", 
            "name": "Sarah Johnson",
            "phone": "+2348023456789",
            "email": "sarah.johnson@realestate.com",
            "status": "active",
            "zone": "Victoria Island",
            "specializations": ["Luxury Properties", "Commercial"],
            "experience_years": 8,
            "rating": 4.9,
            "total_inspections": 220,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
    ]
    
    for agent in sample_agents:
        db_service.insert_document("agents", agent)
    
    # 2. PROPERTIES COLLECTION
    print("Creating properties collection...")
    db_service.create_index("properties", "property_id", unique=True)
    db_service.create_index("properties", "status")
    db_service.create_index("properties", "property_type")
    db_service.create_index("properties", "location")
    db_service.create_index("properties", "price_range")
    
    # Sample properties data
    sample_properties = [
        {
            "property_id": "prop_001",
            "title": "3-Bedroom Luxury Apartment",
            "address": "123 Lekki Phase 1, Lagos",
            "property_type": "Apartment",
            "bedrooms": 3,
            "bathrooms": 2,
            "price": 50000000,
            "currency": "NGN",
            "area": "150 sqm",
            "location": "Lekki",
            "status": "available",
            "features": ["Swimming Pool", "Gym", "Security"],
            "images": ["image1.jpg", "image2.jpg"],
            "description": "Beautiful 3-bedroom apartment with modern amenities",
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
    ]
    
    for property_data in sample_properties:
        db_service.insert_document("properties", property_data)
    
    # 3. JOBS COLLECTION
    print("Creating jobs collection...")
    db_service.create_index("jobs", "job_id", unique=True)
    db_service.create_index("jobs", "status")
    db_service.create_index("jobs", "property_id")
    db_service.create_index("jobs", "client_id")
    db_service.create_index("jobs", "assigned_agent")
    db_service.create_index("jobs", "inspection_date")
    db_service.create_index("jobs", "created_at")
    
    # 4. CLIENTS COLLECTION
    print("Creating clients collection...")
    db_service.create_index("clients", "client_id", unique=True)
    db_service.create_index("clients", "phone", unique=True)
    db_service.create_index("clients", "email")
    db_service.create_index("clients", "status")
    
    # Sample clients data
    sample_clients = [
        {
            "client_id": "client_001",
            "name": "John Doe",
            "phone": "+2348034567890",
            "email": "john.doe@email.com",
            "status": "active",
            "preferences": {
                "property_types": ["Apartment", "House"],
                "locations": ["Lekki", "Victoria Island"],
                "price_range": {"min": 30000000, "max": 80000000}
            },
            "total_inspections": 3,
            "assigned_agent": "agent_001",
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
    ]
    
    for client in sample_clients:
        db_service.insert_document("clients", client)
    
    # 5. MESSAGES COLLECTION
    print("Creating messages collection...")
    db_service.create_index("messages", "message_id", unique=True)
    db_service.create_index("messages", "job_id")
    db_service.create_index("messages", "agent_phone")
    db_service.create_index("messages", "message_type")
    db_service.create_index("messages", "status")
    db_service.create_index("messages", "created_at")
    
    # 6. INSPECTION_REPORTS COLLECTION
    print("Creating inspection_reports collection...")
    db_service.create_index("inspection_reports", "report_id", unique=True)
    db_service.create_index("inspection_reports", "job_id", unique=True)
    db_service.create_index("inspection_reports", "agent_id")
    db_service.create_index("inspection_reports", "property_id")
    db_service.create_index("inspection_reports", "status")
    db_service.create_index("inspection_reports", "created_at")
    
    # 7. SCHEDULED_TASKS COLLECTION
    print("Creating scheduled_tasks collection...")
    db_service.create_index("scheduled_tasks", "task_id", unique=True)
    db_service.create_index("scheduled_tasks", "job_id")
    db_service.create_index("scheduled_tasks", "task_type")
    db_service.create_index("scheduled_tasks", "status")
    db_service.create_index("scheduled_tasks", "scheduled_time")
    
    # 8. PAYMENTS COLLECTION
    print("Creating payments collection...")
    db_service.create_index("payments", "payment_id", unique=True)
    db_service.create_index("payments", "job_id")
    db_service.create_index("payments", "client_id")
    db_service.create_index("payments", "agent_id")
    db_service.create_index("payments", "status")
    db_service.create_index("payments", "payment_method")
    db_service.create_index("payments", "created_at")
    
    # 9. NOTIFICATIONS COLLECTION
    print("Creating notifications collection...")
    db_service.create_index("notifications", "notification_id", unique=True)
    db_service.create_index("notifications", "recipient_type")  # agent, client, admin
    db_service.create_index("notifications", "recipient_id")
    db_service.create_index("notifications", "notification_type")
    db_service.create_index("notifications", "status")
    db_service.create_index("notifications", "created_at")
    
    # 10. SYSTEM_LOGS COLLECTION
    print("Creating system_logs collection...")
    db_service.create_index("system_logs", "log_id", unique=True)
    db_service.create_index("system_logs", "log_level")
    db_service.create_index("system_logs", "component")
    db_service.create_index("system_logs", "created_at")
    
    print("Database setup completed successfully!")
    print("\nCollections created:")
    print("- agents (with indexes: phone, email, status, zone)")
    print("- properties (with indexes: property_id, status, property_type, location, price_range)")
    print("- jobs (with indexes: job_id, status, property_id, client_id, assigned_agent, inspection_date, created_at)")
    print("- clients (with indexes: client_id, phone, email, status)")
    print("- messages (with indexes: message_id, job_id, agent_phone, message_type, status, created_at)")
    print("- inspection_reports (with indexes: report_id, job_id, agent_id, property_id, status, created_at)")
    print("- scheduled_tasks (with indexes: task_id, job_id, task_type, status, scheduled_time)")
    print("- payments (with indexes: payment_id, job_id, client_id, agent_id, status, payment_method, created_at)")
    print("- notifications (with indexes: notification_id, recipient_type, recipient_id, notification_type, status, created_at)")
    print("- system_logs (with indexes: log_id, log_level, component, created_at)")

if __name__ == "__main__":
    setup_database()
