# VTuber Wiki API

## WARNING: ACADEMIC PROJECT ONLY

**IMPORTANT DISCLAIMER**: This is a college assignment project created for educational purposes only. It is not intended for production use and should not be considered reliable, secure, or suitable for real-world applications (I know it's not LOL).

## Overview

The VTuber API is a RESTful web service built with FastAPI and Supabase that provides information about Virtual YouTubers (VTubers). This API serves as a public database for VTuber profiles, agencies, and related information. It was developed as a college assignment to demonstrate API development skills.

### Key Features

- **Public Read Access**: All GET endpoints are publicly accessible without authentication
- **Protected Write Operations**: POST, PUT, and DELETE operations require Supabase authentication
- **Comprehensive VTuber Data**: Store and retrieve detailed VTuber information including agencies, debut dates, social media links, and tags
- **Search and Filtering**: Search VTubers by name or description, filter by agency
- **Bulk Operations**: Support for creating multiple VTubers in a single request

## Technology Stack

- **Backend**: FastAPI (Python)
- **Database**: Supabase (PostgreSQL)
- **Authentication**: Supabase Auth with JWT tokens
- **Testing**: Postman collection for API testing

## API Endpoints

### Public Endpoints (No Authentication Required)

- `GET /` - API documentation and available endpoints
- `GET /health` - Health check endpoint
- `GET /vtubers` - List all VTubers with pagination and filtering
- `GET /vtubers/{id}` - Get specific VTuber by ID
- `GET /search` - Search VTubers by name or description
- `GET /agencies` - List all available agencies

### Protected Endpoints (Authentication Required)

- `POST /vtubers` - Create a single VTuber
- `POST /vtubers/bulk` - Create multiple VTubers (wrapped array format)
- `POST /vtubers/batch` - Create multiple VTubers (direct array format) -- This is a Work In Progress
- `PUT /vtubers/{id}` - Update VTuber information
- `DELETE /vtubers/{id}` - Delete a VTuber

## Testing Process

### Prerequisites

1. **Supabase Account**: Set up a Supabase project with a `vtubers` table
2. **Environment Setup**: Configure your environment variables
3. **Postman**: Install Postman for API testing

### Environment Configuration

Create a Postman environment with the following variables:

- `api_url`: API base URL (e.g., `http://localhost:8000`)
- `supabase_url`: Your Supabase project URL
- `api_key`: Your Supabase anon/public key
- `access_token`: Will be populated after user authentication
- `user_id`: Will be populated after user authentication
- `vtuber_id`: Will be populated after creating a VTuber

### Step-by-Step Testing Guide

#### Step 1: Test Public Endpoints

1. **API Root**: Verify the API is running by calling `GET /`
2. **Health Check**: Confirm service status with `GET /health`
3. **List VTubers**: Test `GET /vtubers` to see existing data (initially empty)

#### Step 2: Set Up Authentication

1. **Create User Account**: Use the User Auth collection to create a new user
2. **Login**: Authenticate to obtain an access token
3. **Verify Token**: The access token will be automatically saved to your environment

#### Step 3: Test Protected Endpoints

1. **Create Single VTuber**: Use `POST /vtubers` to add one VTuber
2. **Verify Creation**: Check `GET /vtubers` to confirm the VTuber was added
3. **Update VTuber**: Use `PUT /vtubers/{id}` to modify VTuber data
4. **Test Search**: Use `GET /search?q=name` to search for VTubers
5. **List Agencies**: Use `GET /agencies` to see all agencies

#### Step 4: Bulk Operations

1. **Bulk Create**: Use `POST /vtubers/bulk` with wrapped array format
2. **Batch Create**: Use `POST /vtubers/batch` with direct array format (recommended for large datasets) -- WIP
3. **Verify Bulk Data**: Check all VTubers were created successfully

#### Step 5: Cleanup (Optional)

1. **Delete VTubers**: Use `DELETE /vtubers/{id}` to remove test data
2. **Logout**: Use the logout endpoint to invalidate the token

### Sample VTuber Data Structure

```json
{
  "name": "Gawr Gura",
  "agency": "hololive English",
  "debut_date": "2020-09-13",
  "description": "A descendant of the Lost City of Atlantis",
  "image_url": "https://example.com/gura.jpg",
  "youtube_channel": "UCQ0UDLQCjY0rmuxCDE38FGg",
  "twitter_handle": "gawrgura",
  "tags": ["hololive", "english", "shark", "gaming"]
}
```

### Database Schema

The `vtubers` table should have the following structure:

- `id` (UUID, Primary Key)
- `name` (VARCHAR, Required)
- `agency` (VARCHAR, Optional)
- `debut_date` (DATE, Optional)
- `description` (TEXT, Optional)
- `image_url` (TEXT, Optional)
- `youtube_channel` (TEXT, Optional)
- `twitter_handle` (VARCHAR, Optional)
- `tags` (TEXT[], Optional)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

### Error Handling

The API returns appropriate HTTP status codes:

- `200` - Success
- `201` - Resource created
- `400` - Bad request
- `401` - Unauthorized
- `404` - Resource not found
- `500` - Internal server error