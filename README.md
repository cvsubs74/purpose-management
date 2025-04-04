# Purpose CRUD Service

A FastAPI service that provides CRUD operations for managing Purpose entities. Purposes are privacy-related constructs used to capture the reasons for storing sensitive data.

## Features

- Full CRUD operations for Purpose entities
- SQLite database integration
- Comprehensive OpenAPI documentation for all endpoints

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the service:
   ```
   uvicorn app.main:app --reload
   ```

3. Access the API documentation:
   - OpenAPI UI: http://localhost:8000/docs
   - ReDoc UI: http://localhost:8000/redoc
   - OpenAPI JSON: http://localhost:8000/openapi.json

## API Endpoints

- `GET /purposes`: List all purposes
- `GET /purposes/{purpose_id}`: Get a specific purpose
- `POST /purposes`: Create a new purpose
- `PUT /purposes/{purpose_id}`: Update a purpose
- `DELETE /purposes/{purpose_id}`: Delete a purpose
