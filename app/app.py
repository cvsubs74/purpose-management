import os
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
from dotenv import load_dotenv
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

# Load environment variables
load_dotenv()

# Initialize app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///purposes.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///purposes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Create an APISpec
spec = APISpec(
    title="Purpose Management API",
    version="1.0.0",
    openapi_version="3.1.0",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
    info={
        "description": "API for managing privacy-related Purpose entities used to capture reasons for storing sensitive data",
        "contact": {"email": "admin@example.com"},
        "license": {"name": "MIT"},
        "summary": "Privacy Purpose Management API"
    },
)

# Define schema components
spec.components.schema("Purpose", {
    "type": "object",
    "properties": {
        "id": {"type": "integer", "description": "Unique identifier for the purpose", "examples": [1, 2, 3]},
        "name": {"type": "string", "description": "Name of the purpose", "examples": ["Marketing", "Customer Support"]},
        "description": {"type": "string", "description": "Detailed description of the purpose", "examples": ["Storing data for marketing campaigns and analytics"]},
        "is_active": {"type": "boolean", "description": "Whether the purpose is currently active", "examples": [True, False]},
        "created_at": {"type": "string", "format": "date-time", "description": "Timestamp when the purpose was created", "examples": ["2023-01-01T00:00:00Z"]},
        "updated_at": {"type": "string", "format": "date-time", "description": "Timestamp when the purpose was last updated", "examples": ["2023-01-02T00:00:00Z"]}
    },
    "required": ["id", "name", "created_at"],
    "additionalProperties": False
})

spec.components.schema("PurposeCreate", {
    "type": "object",
    "required": ["name"],
    "properties": {
        "name": {"type": "string", "description": "Name of the purpose", "examples": ["Marketing", "Customer Support"], "maxLength": 100},
        "description": {"type": "string", "description": "Detailed description of the purpose", "examples": ["Storing data for marketing campaigns and analytics"]},
        "is_active": {"type": "boolean", "description": "Whether the purpose is currently active", "default": True, "examples": [True, False]}
    },
    "additionalProperties": False
})

spec.components.schema("PurposeUpdate", {
    "type": "object",
    "properties": {
        "name": {"type": "string", "description": "Name of the purpose", "examples": ["Marketing", "Customer Support"], "maxLength": 100},
        "description": {"type": "string", "description": "Detailed description of the purpose", "examples": ["Storing data for marketing campaigns and analytics"]},
        "is_active": {"type": "boolean", "description": "Whether the purpose is currently active", "examples": [True, False]}
    },
    "additionalProperties": False,
    "minProperties": 1
})

# Define the OpenAPI documentation route
@app.route('/api/openapi.json')
def get_openapi_spec():
    # Register all documented endpoints
    with app.test_request_context():
        spec.path(view=index)
        spec.path(view=add_purpose)
        spec.path(view=get_purposes)
        spec.path(view=get_purpose)
        spec.path(view=update_purpose)
        spec.path(view=delete_purpose)
    return jsonify(spec.to_dict())

# Create a route for the OpenAPI UI
@app.route('/api/docs')
def api_docs():
    return render_template('openapi.html')

# Purpose Model
class Purpose(db.Model):
    __tablename__ = 'purposes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, name, description, is_active=True):
        self.name = name
        self.description = description
        self.is_active = is_active

# Purpose Schema
class PurposeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'is_active', 'created_at', 'updated_at')
        model = Purpose

# Initialize schemas
purpose_schema = PurposeSchema()
purposes_schema = PurposeSchema(many=True)

# Routes
@app.route('/')
def index():
    """
    Home endpoint that returns API information
    ---
    get:
      summary: Home endpoint
      description: Returns basic API information
      tags:
        - root
      responses:
        200:
          description: Welcome message with links to documentation
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: Welcome to the Purpose Management API
                  documentation:
                    type: string
                    example: http://localhost:8000/api/docs
    """
    return jsonify({
        'message': 'Welcome to the Purpose Management API',
        'documentation': f'{request.url_root.rstrip("/")}/api/docs'
    })

# Create a Purpose
@app.route('/purposes', methods=['POST'])
def add_purpose():
    """
    Create a new purpose
    ---
    post:
      summary: Create a new purpose
      description: Create a new purpose entity
      tags:
        - purposes
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - name
              properties:
                name:
                  type: string
                  description: Name of the purpose
                  example: Marketing
                description:
                  type: string
                  description: Detailed description of the purpose
                  example: Storing data for marketing campaigns and analytics
                is_active:
                  type: boolean
                  description: Whether the purpose is currently active
                  default: true
                  example: true
      responses:
        201:
          description: Purpose created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Purpose'
        409:
          description: Purpose with this name already exists
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: Purpose with name 'Marketing' already exists
        400:
          description: Invalid input
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: Error message
    """
    try:
        name = request.json['name']
        description = request.json.get('description', '')
        is_active = request.json.get('is_active', True)
        
        # Check if purpose with same name already exists
        existing_purpose = Purpose.query.filter_by(name=name).first()
        if existing_purpose:
            return jsonify({'message': f"Purpose with name '{name}' already exists"}), 409
        
        new_purpose = Purpose(name, description, is_active)
        
        db.session.add(new_purpose)
        db.session.commit()
        
        return purpose_schema.jsonify(new_purpose), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400

# Get All Purposes
@app.route('/purposes', methods=['GET'])
def get_purposes():
    """
    Get all purposes with optional filtering
    ---
    get:
      summary: Get all purposes
      description: Retrieve a list of all purposes with optional filtering
      tags:
        - purposes
      parameters:
        - in: query
          name: name
          schema:
            type: string
          description: Filter purposes by name (partial match)
        - in: query
          name: is_active
          schema:
            type: boolean
          description: Filter purposes by active status
        - in: query
          name: skip
          schema:
            type: integer
            default: 0
          description: Number of records to skip (for pagination)
        - in: query
          name: limit
          schema:
            type: integer
            default: 100
          description: Maximum number of records to return
      responses:
        200:
          description: A list of purposes
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Purpose'
    """
    query = Purpose.query
    
    # Apply filters if provided
    name_filter = request.args.get('name')
    if name_filter:
        query = query.filter(Purpose.name.ilike(f'%{name_filter}%'))
    
    is_active_filter = request.args.get('is_active')
    if is_active_filter is not None:
        is_active_bool = is_active_filter.lower() == 'true'
        query = query.filter_by(is_active=is_active_bool)
    
    # Apply pagination
    skip = request.args.get('skip', default=0, type=int)
    limit = request.args.get('limit', default=100, type=int)
    
    all_purposes = query.offset(skip).limit(limit).all()
    result = purposes_schema.dump(all_purposes)
    
    return jsonify(result)

# Get Single Purpose
@app.route('/purposes/<id>', methods=['GET'])
def get_purpose(id):
    """
    Get a specific purpose by ID
    ---
    get:
      summary: Get a specific purpose
      description: Retrieve a specific purpose by ID
      tags:
        - purposes
      parameters:
        - in: path
          name: id
          schema:
            type: integer
          required: true
          description: ID of the purpose to retrieve
      responses:
        200:
          description: Purpose details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Purpose'
        404:
          description: Purpose not found
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: Purpose with ID 1 not found
    """
    purpose = Purpose.query.get(id)
    
    if not purpose:
        return jsonify({'message': f'Purpose with ID {id} not found'}), 404
        
    return purpose_schema.jsonify(purpose)

# Update a Purpose
@app.route('/purposes/<id>', methods=['PUT'])
def update_purpose(id):
    """
    Update an existing purpose
    ---
    put:
      summary: Update a purpose
      description: Update an existing purpose
      tags:
        - purposes
      parameters:
        - in: path
          name: id
          schema:
            type: integer
          required: true
          description: ID of the purpose to update
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                name:
                  type: string
                  description: Name of the purpose
                  example: Marketing
                description:
                  type: string
                  description: Detailed description of the purpose
                  example: Storing data for marketing campaigns and analytics
                is_active:
                  type: boolean
                  description: Whether the purpose is currently active
                  example: true
      responses:
        200:
          description: Purpose updated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Purpose'
        404:
          description: Purpose not found
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: Purpose with ID 1 not found
        409:
          description: Purpose with this name already exists
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: Purpose with name 'Marketing' already exists
    """
    purpose = Purpose.query.get(id)
    
    if not purpose:
        return jsonify({'message': f'Purpose with ID {id} not found'}), 404
    
    # Get the update data
    name = request.json.get('name')
    description = request.json.get('description')
    is_active = request.json.get('is_active')
    
    # Check if updating to a name that already exists
    if name and name != purpose.name:
        existing_purpose = Purpose.query.filter_by(name=name).first()
        if existing_purpose:
            return jsonify({'message': f"Purpose with name '{name}' already exists"}), 409
    
    # Update fields if provided
    if name:
        purpose.name = name
    if description is not None:
        purpose.description = description
    if is_active is not None:
        purpose.is_active = is_active
    
    db.session.commit()
    
    return purpose_schema.jsonify(purpose)

# Delete Purpose
@app.route('/purposes/<id>', methods=['DELETE'])
def delete_purpose(id):
    """
    Delete a purpose
    ---
    delete:
      summary: Delete a purpose
      description: Delete a purpose by ID
      tags:
        - purposes
      parameters:
        - in: path
          name: id
          schema:
            type: integer
          required: true
          description: ID of the purpose to delete
      responses:
        200:
          description: Purpose deleted successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Purpose'
        404:
          description: Purpose not found
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: Purpose with ID 1 not found
    """
    purpose = Purpose.query.get(id)
    
    if not purpose:
        return jsonify({'message': f'Purpose with ID {id} not found'}), 404
    
    db.session.delete(purpose)
    db.session.commit()
    
    return purpose_schema.jsonify(purpose)

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
