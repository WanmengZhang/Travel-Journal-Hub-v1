"""
Travel Journal Hub - Flask Backend Application
Manages journal entries with MySQL database integration
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Database configuration
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'database': os.environ.get('DB_NAME', 'travel_journal')
}

def get_db_connection():
    """Create and return a database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def init_db():
    """Initialize the database and create tables if they don't exist"""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            
            # Create database if it doesn't exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
            cursor.execute(f"USE {DB_CONFIG['database']}")
            
            # Create journal_entries table
            create_table_query = """
            CREATE TABLE IF NOT EXISTS journal_entries (
                id INT AUTO_INCREMENT PRIMARY KEY,
                destination VARCHAR(255) NOT NULL,
                start_date DATE NOT NULL,
                end_date DATE NOT NULL,
                description TEXT,
                highlights TEXT,
                photo_links TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
            """
            cursor.execute(create_table_query)
            connection.commit()
            print("Database initialized successfully")
        except Error as e:
            print(f"Error initializing database: {e}")
        finally:
            cursor.close()
            connection.close()

# Routes for serving HTML pages
@app.route('/')
def index():
    """Serve the homepage"""
    return render_template('index.html')

@app.route('/journals')
def journals():
    """Serve the My Journals page"""
    return render_template('journals.html')

@app.route('/editor')
def editor():
    """Serve the Entry Editor page"""
    return render_template('editor.html')

# API Routes
@app.route('/api/entries', methods=['GET'])
def get_entries():
    """Get all journal entries"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, destination, start_date, end_date, description, 
                   highlights, photo_links, created_at, updated_at
            FROM journal_entries
            ORDER BY start_date DESC
        """)
        entries = cursor.fetchall()
        
        # Convert date objects to strings
        for entry in entries:
            if entry['start_date']:
                entry['start_date'] = entry['start_date'].strftime('%Y-%m-%d')
            if entry['end_date']:
                entry['end_date'] = entry['end_date'].strftime('%Y-%m-%d')
            if entry['created_at']:
                entry['created_at'] = entry['created_at'].strftime('%Y-%m-%d %H:%M:%S')
            if entry['updated_at']:
                entry['updated_at'] = entry['updated_at'].strftime('%Y-%m-%d %H:%M:%S')
        
        return jsonify(entries), 200
    except Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Failed to retrieve entries'}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/api/entries/<int:entry_id>', methods=['GET'])
def get_entry(entry_id):
    """Get a specific journal entry by ID"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, destination, start_date, end_date, description, 
                   highlights, photo_links, created_at, updated_at
            FROM journal_entries
            WHERE id = %s
        """, (entry_id,))
        entry = cursor.fetchone()
        
        if not entry:
            return jsonify({'error': 'Entry not found'}), 404
        
        # Convert date objects to strings
        if entry['start_date']:
            entry['start_date'] = entry['start_date'].strftime('%Y-%m-%d')
        if entry['end_date']:
            entry['end_date'] = entry['end_date'].strftime('%Y-%m-%d')
        if entry['created_at']:
            entry['created_at'] = entry['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        if entry['updated_at']:
            entry['updated_at'] = entry['updated_at'].strftime('%Y-%m-%d %H:%M:%S')
        
        return jsonify(entry), 200
    except Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Failed to retrieve entry'}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/api/entries', methods=['POST'])
def create_entry():
    """Create a new journal entry"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['destination', 'start_date', 'end_date']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO journal_entries 
            (destination, start_date, end_date, description, highlights, photo_links)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            data['destination'],
            data['start_date'],
            data['end_date'],
            data.get('description', ''),
            data.get('highlights', ''),
            data.get('photo_links', '')
        )
        cursor.execute(query, values)
        connection.commit()
        
        entry_id = cursor.lastrowid
        return jsonify({'id': entry_id, 'message': 'Entry created successfully'}), 201
    except Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Failed to create entry'}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/api/entries/<int:entry_id>', methods=['PUT'])
def update_entry(entry_id):
    """Update an existing journal entry"""
    data = request.get_json()
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor()
        
        # Check if entry exists
        cursor.execute("SELECT id FROM journal_entries WHERE id = %s", (entry_id,))
        if not cursor.fetchone():
            return jsonify({'error': 'Entry not found'}), 404
        
        # Update entry
        query = """
            UPDATE journal_entries 
            SET destination = %s, start_date = %s, end_date = %s, 
                description = %s, highlights = %s, photo_links = %s
            WHERE id = %s
        """
        values = (
            data.get('destination'),
            data.get('start_date'),
            data.get('end_date'),
            data.get('description', ''),
            data.get('highlights', ''),
            data.get('photo_links', ''),
            entry_id
        )
        cursor.execute(query, values)
        connection.commit()
        
        return jsonify({'message': 'Entry updated successfully'}), 200
    except Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Failed to update entry'}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/api/entries/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    """Delete a journal entry"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor()
        
        # Check if entry exists
        cursor.execute("SELECT id FROM journal_entries WHERE id = %s", (entry_id,))
        if not cursor.fetchone():
            return jsonify({'error': 'Entry not found'}), 404
        
        # Delete entry
        cursor.execute("DELETE FROM journal_entries WHERE id = %s", (entry_id,))
        connection.commit()
        
        return jsonify({'message': 'Entry deleted successfully'}), 200
    except Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Failed to delete entry'}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    init_db()
    # Use environment variable to control debug mode (default to False for security)
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
