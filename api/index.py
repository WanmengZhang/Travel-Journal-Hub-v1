"""
Vercel Serverless Function Entry Point
This file imports and exposes the Flask app for Vercel deployment
"""

import sys
import os

# Add parent directory to path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set SQLite mode for Vercel (serverless environment)
os.environ['USE_SQLITE'] = 'true'

# Import Flask app
from app import app, init_db

# Initialize database on cold start
# In serverless, this runs once per function instance
_initialized = False

def ensure_db_initialized():
    """Ensure database is initialized (idempotent)"""
    global _initialized
    if not _initialized:
        try:
            init_db()
            _initialized = True
            print("Database initialized successfully")
        except Exception as e:
            print(f"Database initialization warning: {e}")
            # Continue anyway - tables might already exist

# Initialize on import
ensure_db_initialized()

# Vercel expects 'app' variable
# This is the WSGI application that Vercel will call
app = app
