from app.app import app, db, Purpose

# Sample purposes
sample_purposes = [
    {
        "name": "Marketing",
        "description": "Storing data for marketing campaigns, analytics, and customer outreach",
        "is_active": True
    },
    {
        "name": "Customer Support",
        "description": "Storing data to provide customer service and support",
        "is_active": True
    },
    {
        "name": "Product Improvement",
        "description": "Storing data to analyze usage patterns and improve product features",
        "is_active": True
    },
    {
        "name": "Legal Compliance",
        "description": "Storing data to comply with legal and regulatory requirements",
        "is_active": True
    },
    {
        "name": "Historical Research",
        "description": "Storing data for historical research and archival purposes",
        "is_active": False
    }
]

# Initialize the database and add sample data
with app.app_context():
    # Create tables
    db.create_all()
    
    # Check if data already exists
    existing_purposes = Purpose.query.all()
    if not existing_purposes:
        # Add sample purposes to the database
        for purpose_data in sample_purposes:
            purpose = Purpose(
                name=purpose_data['name'],
                description=purpose_data['description'],
                is_active=purpose_data['is_active']
            )
            db.session.add(purpose)
        
        # Commit the changes
        db.session.commit()
        print("Sample purposes added to the database.")
    else:
        print("Database already contains purposes. No sample data added.")
