import os
import logging
from flask import Flask
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the Flask application
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure secret key
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Import routes after app is created to avoid circular imports
from routes import *

# Note: For MVP we're using in-memory storage
# In the future, we'll implement PostgreSQL integration
# app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
