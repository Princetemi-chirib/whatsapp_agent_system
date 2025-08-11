# WhatsApp Agent Dispatch System - API Documentation

## Overview
This document provides complete API documentation for integrating the WhatsApp Agent Dispatch & Inspection Notification System with your live real estate website.

## Base URL
```
http://your-domain.com/api
```

## Authentication
Currently, the API uses simple API key authentication. Add this header to all requests:
```
Authorization: Bearer YOUR_API_KEY
```

## Database Collections & Schema

### 1. AGENTS Collection
Stores all real estate agents who can receive inspection requests.

**Schema:**
```json
{
  "_id": "ObjectId",
  "agent_id": "string (unique)",
  "name": "string",
  "phone": "string (unique)",
  "email": "string (unique)",
  "status": "active|inactive|suspended",
  "zone": "string",
  "specializations": ["string"],
  "experience_years": "number",
  "rating": "number",
  "total_inspections": "number",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### 2. PROPERTIES Collection
Stores property details from your real estate platform.

**Schema:**
```json
{
  "_id": "ObjectId",
  "property_id": "string (unique)",
  "title": "string",
  "address": "string",
  "property_type": "Apartment|House|Commercial|Land",
  "bedrooms": "number",
  "bathrooms": "number",
  "price": "number",
  "currency": "string",
  "area": "string",
  "location": "string",
  "status": "available|sold|rented|pending",
  "features": ["string"],
  "images": ["string"],
  "description": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### 3. JOBS Collection
Stores inspection requests and their status.

**Schema:**
```json
{
  "_id": "ObjectId",
  "job_id": "string (unique)",
  "property_id": "string",
  "client_id": "string",
  "inspection_date": "string (YYYY-MM-DD)",
  "inspection_time": "string (HH:MM)",
  "status": "pending|assigned|approved|completed|cancelled",
  "assigned_agent": "string (phone)",
  "notes": "string",
  "property_details": "object",
  "client_details": "object",
  "assigned_at": "datetime",
  "approved_at": "datetime",
  "completed_at": "datetime",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### 4. CLIENTS Collection
Stores client information and preferences.

**Schema:**
```json
{
  "_id": "ObjectId",
  "client_id": "string (unique)",
  "name": "string",
  "phone": "string (unique)",
  "email": "string",
  "status": "active|inactive",
  "preferences": {
    "property_types": ["string"],
    "locations": ["string"],
    "price_range": {
      "min": "number",
      "max": "number"
    }
  },
  "total_inspections": "number",
  "assigned_agent": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### 5. MESSAGES Collection
Logs all WhatsApp interactions.

**Schema:**
```json
{
  "_id": "ObjectId",
  "message_id": "string (unique)",
  "job_id": "string",
  "agent_phone": "string",
  "message_type": "inspection_request|confirmation|reminder|completion",
  "direction": "outbound|inbound",
  "content": "string",
  "status": "sent|delivered|read|failed",
  "twilio_sid": "string",
  "created_at": "datetime"
}
```

## API Endpoints

### Inspection Jobs

#### 1. Create Inspection Request
**POST** `/jobs/`

**Request Body:**
```json
{
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
}
```

**Response:**
```json
{
  "id": "job_789",
  "property_id": "prop_123",
  "client_id": "client_456",
  "inspection_date": "2024-01-15",
  "inspection_time": "14:00",
  "status": "pending",
  "assigned_agent": null,
  "notes": "Client prefers afternoon viewing",
  "property_details": {...},
  "client_details": {...},
  "created_at": "2024-01-10T10:30:00Z",
  "updated_at": "2024-01-10T10:30:00Z"
}
```

#### 2. Get All Jobs
**GET** `/jobs/`

**Query Parameters:**
- `status` (optional): Filter by status
- `agent_phone` (optional): Filter by assigned agent
- `client_id` (optional): Filter by client
- `property_id` (optional): Filter by property

**Response:**
```json
[
  {
    "id": "job_789",
    "property_id": "prop_123",
    "client_id": "client_456",
    "inspection_date": "2024-01-15",
    "inspection_time": "14:00",
    "status": "pending",
    "assigned_agent": null,
    "property_details": {...},
    "client_details": {...},
    "created_at": "2024-01-10T10:30:00Z",
    "updated_at": "2024-01-10T10:30:00Z"
  }
]
```

#### 3. Get Job by ID
**GET** `/jobs/{job_id}`

**Response:**
```json
{
  "id": "job_789",
  "property_id": "prop_123",
  "client_id": "client_456",
  "inspection_date": "2024-01-15",
  "inspection_time": "14:00",
  "status": "assigned",
  "assigned_agent": "+2348012345678",
  "property_details": {...},
  "client_details": {...},
  "created_at": "2024-01-10T10:30:00Z",
  "updated_at": "2024-01-10T10:30:00Z"
}
```

#### 4. Update Job
**PUT** `/jobs/{job_id}`

**Request Body:**
```json
{
  "inspection_date": "2024-01-16",
  "inspection_time": "15:00",
  "notes": "Updated notes"
}
```

#### 5. Delete Job
**DELETE** `/jobs/{job_id}`

#### 6. Approve Schedule
**POST** `/jobs/{job_id}/approve_schedule`

#### 7. Complete Inspection
**POST** `/jobs/{job_id}/complete_inspection`

### Agent Management

#### 1. Get Jobs by Agent
**GET** `/jobs/agent/{agent_phone}/jobs`

#### 2. Get Jobs by Client
**GET** `/jobs/client/{client_id}/jobs`

#### 3. Get Jobs by Property
**GET** `/jobs/property/{property_id}/jobs`

### Webhooks

#### 1. Twilio WhatsApp Webhook
**POST** `/webhooks/twilio/whatsapp`

**Form Data:**
- `From`: WhatsApp number (e.g., "whatsapp:+2348012345678")
- `Body`: Message content

**Response:**
```json
{
  "status": "success",
  "message": "Job assigned"
}
```

#### 2. Webhook Status
**GET** `/webhooks/twilio/status`

## Integration Workflow

### 1. Website Integration Points

#### A. Property Listing Page
When a client clicks "Request Inspection" on your property listing:

```javascript
// Frontend JavaScript
async function requestInspection(propertyId, clientData) {
  const response = await fetch('/api/jobs/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer YOUR_API_KEY'
    },
    body: JSON.stringify({
      property: {
        property_id: propertyId,
        title: property.title,
        address: property.address,
        property_type: property.type,
        bedrooms: property.bedrooms,
        bathrooms: property.bathrooms,
        price: property.price,
        area: property.area
      },
      client: {
        client_id: clientData.id,
        name: clientData.name,
        phone: clientData.phone,
        email: clientData.email
      },
      inspection_date: selectedDate,
      inspection_time: selectedTime,
      notes: additionalNotes
    })
  });
  
  const result = await response.json();
  return result;
}
```

#### B. Client Dashboard
Show inspection status to clients:

```javascript
// Get client's inspection requests
async function getClientInspections(clientId) {
  const response = await fetch(`/api/jobs/client/${clientId}/jobs`, {
    headers: {
      'Authorization': 'Bearer YOUR_API_KEY'
    }
  });
  
  const inspections = await response.json();
  return inspections;
}
```

#### C. Admin Dashboard
Monitor all inspection requests:

```javascript
// Get all pending inspections
async function getPendingInspections() {
  const response = await fetch('/api/jobs/?status=pending', {
    headers: {
      'Authorization': 'Bearer YOUR_API_KEY'
    }
  });
  
  const pendingJobs = await response.json();
  return pendingJobs;
}
```

### 2. WhatsApp Commands for Agents

Agents receive WhatsApp messages and can respond with:

- **YES** - Accept inspection request
- **CONFIRM** - Confirm inspection schedule  
- **COMPLETE** - Mark inspection as completed

### 3. Status Flow

1. **pending** → Client requests inspection
2. **assigned** → Agent accepts with "YES"
3. **approved** → Agent confirms with "CONFIRM"
4. **completed** → Agent completes with "COMPLETE"

## Environment Variables

```env
# FastAPI Configuration
HOST=0.0.0.0
PORT=5000

# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=whatsapp_agent_system

# Twilio WhatsApp API Configuration
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_NUMBER=+14155238886

# Security
SECRET_KEY=your_secret_key_here
API_KEY=your_api_key_for_website_integration

# Logging
LOG_LEVEL=INFO
```

## Error Handling

All endpoints return appropriate HTTP status codes:

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `404` - Not Found
- `500` - Internal Server Error

Error responses include:
```json
{
  "detail": "Error message description"
}
```

## Rate Limiting

Consider implementing rate limiting for production:
- 100 requests per minute per IP
- 1000 requests per hour per API key

## Security Considerations

1. **API Key Authentication** - Use secure API keys
2. **HTTPS** - Always use HTTPS in production
3. **Input Validation** - All inputs are validated
4. **CORS** - Configure CORS for your domain
5. **Rate Limiting** - Implement rate limiting
6. **Logging** - Monitor API usage

## Testing

### Test Inspection Request
```bash
curl -X POST "http://localhost:5000/api/jobs/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "property": {
      "property_id": "test_prop_001",
      "title": "Test Property",
      "address": "123 Test Street",
      "property_type": "Apartment",
      "bedrooms": 2,
      "bathrooms": 1,
      "price": 30000000,
      "area": "100 sqm"
    },
    "client": {
      "client_id": "test_client_001",
      "name": "Test Client",
      "phone": "+2348012345678",
      "email": "test@example.com"
    },
    "inspection_date": "2024-01-20",
    "inspection_time": "10:00",
    "notes": "Test inspection request"
  }'
```

This API documentation provides everything needed to integrate the WhatsApp Agent Dispatch System with your live real estate website.

