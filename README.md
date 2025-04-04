# Purpose Management API

A Flask-based REST API service that provides CRUD operations for managing Purpose entities. Purposes are privacy-related constructs used to capture the reasons for storing sensitive data.

## Features

- Full CRUD operations for Purpose entities
- SQLite database integration
- Comprehensive OpenAPI 3.1 documentation for all endpoints
- Interactive API documentation UI

## Getting Started

### Clone the Repository

```bash
# Clone the repository
git clone https://github.com/cvsubs74/purpose-management.git

# Navigate to the project directory
cd purpose-management
```

### Set Up Virtual Environment

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt
```

### Initialize the Database

```bash
# Initialize the SQLite database with sample data
python init_db.py
```

### Run the Application

```bash
# Start the Flask application
python run.py
```

The application will be running at http://127.0.0.1:8000

### Access the API

- **Main API**: http://127.0.0.1:8000
- **OpenAPI Documentation UI**: http://127.0.0.1:8000/api/docs
- **OpenAPI 3.1 Specification**: http://127.0.0.1:8000/api/openapi.json

## API Endpoints

- `GET /purposes`: List all purposes with optional filtering and pagination
- `GET /purposes/{id}`: Get a specific purpose by ID
- `POST /purposes`: Create a new purpose
- `PUT /purposes/{id}`: Update an existing purpose
- `DELETE /purposes/{id}`: Delete a purpose

## Purpose Entity

The Purpose entity represents privacy-related purposes for storing sensitive data with the following fields:

- `id`: Unique identifier
- `name`: Name of the purpose (unique)
- `description`: Detailed description
- `is_active`: Whether the purpose is currently active
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

## Development

### Running in Development Mode

```bash
# With Flask CLI
export FLASK_APP=app.app
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=8000
```

### Production Deployment

For production, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 "app.app:app"
```
