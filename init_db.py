# Create database tables (only need to run once).
# Imports
from app import app, db

with app.app_context():
    db.create_all()
    print("Database tables created.")
