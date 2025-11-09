"""
Vercel Serverless Function Entry Point
This file imports and exposes the Flask app for Vercel deployment
"""

import sys
import os

# Add parent directory to path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Initialize database on first import
from app import init_db
try:
    init_db()
except Exception as e:
    print(f"Database initialization error (may be expected in serverless): {e}")

# Vercel expects a variable named 'app' or a handler function
# Export the Flask app directly
app = app
