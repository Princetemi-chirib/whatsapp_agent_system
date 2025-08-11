# WhatsApp Agent Dispatch & Inspection Notification System

A FastAPI-based REST API system for managing real estate inspection jobs with automated WhatsApp notifications via Twilio, MongoDB storage, and intelligent agent assignment.

## Project Overview

This system connects a real estate platform with field agents using Twilio's WhatsApp API to:

- Send inspection requests for properties to all available agents
- Allow the first agent to respond "YES" to claim the job
- Automatically send property details to the assigned agent
- Notify all other agents that the request is no longer available
- Confirm booking when the assigned agent approves the viewing schedule
- Send reminders at the scheduled inspection time
- Handle multiple property requests for the same client

## Project Structure

```
whatsapp_agent_system/
│
├── app/
│   ├── __init__.py
│   ├── main.py                         # FastAPI entry point
│   │
│   ├── models/
│   │   └── __init__.py                 # Could hold MongoDB schema helpers or Pydantic models
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── jobs.py                     # Inspection job management endpoints
│   │   └── webhooks.py                 # Twilio WhatsApp webhook handlers
│   │
│   └── services/
│       ├── __init__.py
│       ├── job_service.py              # Business logic for inspection jobs
│       ├── whatsapp_service.py         # Twilio WhatsApp API integration
│       ├── database.py                 # MongoDB connection and operations
│       └── scheduler.py                # Inspection reminder scheduling
│
├── .env
├── requirements.txt
└── README.md
```

## Key Features

- **Twilio WhatsApp Integration**: Automated messaging via Twilio's WhatsApp Business API
- **FastAPI Framework**: Modern, fast web framework with automatic API documentation
- **MongoDB Integration**: Persistent storage for jobs, agents, properties, and messages
- **Intelligent Agent Assignment**: First-come-first-served job assignment system
- **Automated Scheduling**: Inspection reminders and follow-up notifications
- **Webhook Processing**: Real-time handling of agent responses via Twilio webhooks
- **Multiple Property Support**: Continuity for clients booking multiple properties
- **Real-time Status Updates**: Live job status tracking and notifications

## System Workflow

### 1. Client Requests Inspection
- Residence platform sends API request with property details and client information
- System creates inspection job and notifies all active agents

### 2. Agent Assignment
- All agents receive WhatsApp message with property details
- First agent to reply "YES" gets assigned the job
- Other agents receive "Job already assigned" notification

### 3. Schedule Confirmation
- Assigned agent receives property and client details
- Agent confirms schedule by replying "CONFIRM"
- System schedules inspection reminder

### 4. Inspection Reminder
- System sends reminder 30 minutes before scheduled inspection
- Agent can mark inspection as completed by replying "COMPLETE"

### 5. Multiple Properties
- If client books additional properties, same agent gets priority notification
- Maintains continuity of service for existing clients

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd whatsapp_agent_system
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up MongoDB:
   - Install MongoDB locally or use MongoDB Atlas
   - Update MongoDB connection string in `.env` file

5. Configure Twilio:
   - Sign up for Twilio account
   - Get WhatsApp Business API access
   - Update Twilio credentials in `.env` file

6. Configure environment variables:
   - Update the `.env` file with your configuration
   - Add your Twilio credentials
   - Set your MongoDB connection string

## Usage

### Running the Application

```bash
# Development
python -m app.main

# Production with uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 5000

# With reload for development
uvicorn app.main:app --reload --host 0.0.0.0 --port 5000
```

The API will be available at `http://localhost:5000`
API documentation will be available at `http://localhost:5000/docs`

### API Endpoints

#### Inspection Jobs

- `POST /api/jobs/` - Create new inspection request
- `GET /api/jobs/` - Get all inspection jobs
- `GET /api/jobs/{job_id}` - Get specific inspection job
- `PUT /api/jobs/{job_id}` - Update inspection job
- `DELETE /api/jobs/{job_id}` - Delete inspection job
- `POST /api/jobs/{job_id}/approve_schedule` - Approve inspection schedule
- `POST /api/jobs/{job_id}/complete_inspection` - Mark inspection as completed

#### Agent Management

- `GET /api/jobs/agent/{agent_phone}/jobs` - Get jobs assigned to specific agent
- `GET /api/jobs/client/{client_id}/jobs` - Get jobs for specific client
- `GET /api/jobs/property/{property_id}/jobs` - Get jobs for specific property

#### Webhooks

- `POST /api/webhooks/twilio/whatsapp` - Twilio WhatsApp webhook endpoint
- `GET /api/webhooks/twilio/status` - Webhook status check

#### Health Check

- `GET /` - API root
- `GET /health` - Health check endpoint

### Example Inspection Request

```bash
curl -X POST "http://localhost:5000/api/jobs/" \
  -H "Content-Type: application/json" \
  -d '{
    "property": {
      "property_id": "prop_123",
      "title": "3-Bedroom Apartment",
      "address": "123 Lekki Phase 1, Lagos",
      "property_type": "Apartment",
      "bedrooms": 3,
      "bathrooms": 2,
      "price": 50000000,
      "area": "150 sqm"
    },
    "client": {
      "client_id": "client_456",
      "name": "John Doe",
      "phone": "+2348012345678",
      "email": "john.doe@example.com"
    },
    "inspection_date": "2024-01-15",
    "inspection_time": "14:00",
    "notes": "Client prefers afternoon viewing"
  }'
```

### WhatsApp Commands for Agents

- **YES** - Accept inspection request
- **CONFIRM** - Confirm inspection schedule
- **COMPLETE** - Mark inspection as completed

## Environment Variables

```env
# FastAPI Configuration
HOST=0.0.0.0
PORT=5000

# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=whatsapp_agent_system

# Twilio WhatsApp API Configuration
TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
TWILIO_WHATSAPP_NUMBER=+14155238886

# Security
SECRET_KEY=your_secret_key_here_change_in_production

# Logging
LOG_LEVEL=INFO
```

## Database Collections

- **agents** - Agent profiles and WhatsApp numbers
- **properties** - Property details from residence platform
- **jobs** - Inspection requests with status tracking
- **messages** - Logs of all WhatsApp interactions

## Twilio Setup

1. Create a Twilio account
2. Enable WhatsApp Business API
3. Configure webhook URL: `https://your-domain.com/api/webhooks/twilio/whatsapp`
4. Add your Twilio credentials to `.env` file
5. Test webhook connectivity

## Development

### Project Structure

- **`app/main.py`**: FastAPI application setup and configuration
- **`app/routes/`**: API route definitions with Pydantic models
- **`app/services/`**: Business logic and external service integrations
- **`app/models/`**: Data models (ready for MongoDB schema helpers)

### Adding New Features

1. **New Routes**: Add new routers in `app/routes/`
2. **New Services**: Create service classes in `app/services/`
3. **New Models**: Define Pydantic models in route files or `app/models/`

## Future Enhancements

- [ ] User authentication and authorization (JWT)
- [ ] Real-time WebSocket notifications
- [ ] File upload support for inspection reports
- [ ] Advanced agent filtering and matching
- [ ] Inspection report templates
- [ ] Multi-language support
- [ ] Advanced analytics and reporting
- [ ] Mobile app integration
- [ ] Email notifications as fallback
- [ ] Integration with external CRM systems
- [ ] Payment integration for inspection fees
- [ ] GPS tracking for agent location
- [ ] Photo upload during inspections

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
