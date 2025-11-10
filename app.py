"""
Travel Journal Hub - Flask Backend Application
Manages journal entries with MySQL database integration
Supports SQLite as fallback for development/testing
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime

# Try MySQL first, fall back to SQLite if unavailable
USE_SQLITE = os.environ.get('USE_SQLITE', 'false').lower() == 'true'

# Always import sqlite3 as fallback
import sqlite3

if not USE_SQLITE:
    try:
        import mysql.connector
        from mysql.connector import Error as MySQLError
        DB_TYPE = 'mysql'
        print("✓ MySQL connector available, attempting to use MySQL")
    except ImportError:
        print("⚠ MySQL connector not available, falling back to SQLite")
        USE_SQLITE = True
        DB_TYPE = 'sqlite'
else:
    DB_TYPE = 'sqlite'
    print("✓ Using SQLite (USE_SQLITE=true)")

# SQLite configuration (always needed as fallback)
if os.environ.get('VERCEL'):
    SQLITE_DB_PATH = '/tmp/travel_journal.db'
else:
    SQLITE_DB_PATH = os.environ.get('SQLITE_DB_PATH', 'travel_journal.db')

app = Flask(__name__)
CORS(app)

# Database configuration
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'database': os.environ.get('DB_NAME', 'travel_journal')
}

def dict_cursor(connection):
    """Get a cursor that returns dictionaries for both MySQL and SQLite"""
    if DB_TYPE == 'sqlite':
        cursor = connection.cursor()
        cursor.row_factory = sqlite3.Row
        return cursor
    else:
        return connection.cursor(dictionary=True)

def get_db_connection():
    """Create and return a database connection (MySQL or SQLite with auto-fallback)"""
    global DB_TYPE  # Allow switching DB_TYPE at runtime
    
    if DB_TYPE == 'sqlite':
        try:
            connection = sqlite3.connect(SQLITE_DB_PATH)
            connection.row_factory = sqlite3.Row  # Enable column access by name
            return connection
        except sqlite3.Error as e:
            print(f"❌ Error connecting to SQLite: {e}")
            return None
    else:
        # Try MySQL first
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            return connection
        except MySQLError as e:
            print(f"⚠️  MySQL connection failed: {e}")
            print(f"🔄 Auto-fallback: Switching to SQLite...")
            
            # Auto-fallback to SQLite
            DB_TYPE = 'sqlite'
            try:
                connection = sqlite3.connect(SQLITE_DB_PATH)
                connection.row_factory = sqlite3.Row
                print(f"✓ Successfully connected to SQLite: {SQLITE_DB_PATH}")
                return connection
            except sqlite3.Error as sqlite_e:
                print(f"❌ SQLite fallback also failed: {sqlite_e}")
                return None

def init_db():
    """Initialize the database and create tables if they don't exist (with auto-fallback)"""
    global DB_TYPE
    
    connection = get_db_connection()  # This will auto-fallback if needed
    if not connection:
        print("❌ Failed to initialize database: No connection available")
        return
    
    try:
        cursor = connection.cursor()
        
        if DB_TYPE == 'sqlite':
            # Create journal_entries table for SQLite
            create_table_query = """
            CREATE TABLE IF NOT EXISTS journal_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                destination TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                description TEXT,
                highlights TEXT,
                photo_links TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            cursor.execute(create_table_query)
            connection.commit()
            print(f"✓ SQLite database initialized successfully at {SQLITE_DB_PATH}")
        else:
            # Create database if it doesn't exist (MySQL)
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
            print("✓ MySQL database initialized successfully")
            
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
    finally:
        cursor.close()
        connection.close()

# Routes for serving HTML pages
@app.route('/favicon.ico')
def favicon():
    """Serve favicon or return 204 if not found"""
    from flask import send_from_directory
    import os
    favicon_path = os.path.join(app.root_path, 'static', 'favicon.ico')
    if os.path.exists(favicon_path):
        return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
    else:
        # Return 204 No Content if favicon doesn't exist (prevents 404 error)
        return '', 204

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
        if DB_TYPE == 'sqlite':
            cursor = connection.cursor()
            cursor.execute("""
                SELECT id, destination, start_date, end_date, description, 
                       highlights, photo_links, created_at, updated_at
                FROM journal_entries
                ORDER BY start_date DESC
            """)
            rows = cursor.fetchall()
            # Convert sqlite3.Row to dict
            entries = [dict(row) for row in rows]
        else:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT id, destination, start_date, end_date, description, 
                       highlights, photo_links, created_at, updated_at
                FROM journal_entries
                ORDER BY start_date DESC
            """)
            entries = cursor.fetchall()
        
        # Convert date objects to strings (SQLite stores as strings already)
        for entry in entries:
            if DB_TYPE == 'mysql' and entry.get('start_date'):
                entry['start_date'] = entry['start_date'].strftime('%Y-%m-%d') if hasattr(entry['start_date'], 'strftime') else entry['start_date']
            if DB_TYPE == 'mysql' and entry.get('end_date'):
                entry['end_date'] = entry['end_date'].strftime('%Y-%m-%d') if hasattr(entry['end_date'], 'strftime') else entry['end_date']
            if DB_TYPE == 'mysql' and entry.get('created_at'):
                entry['created_at'] = entry['created_at'].strftime('%Y-%m-%d %H:%M:%S') if hasattr(entry['created_at'], 'strftime') else entry['created_at']
            if DB_TYPE == 'mysql' and entry.get('updated_at'):
                entry['updated_at'] = entry['updated_at'].strftime('%Y-%m-%d %H:%M:%S') if hasattr(entry['updated_at'], 'strftime') else entry['updated_at']
        
        return jsonify(entries), 200
    except Exception as e:
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
        placeholder = '?' if DB_TYPE == 'sqlite' else '%s'
        if DB_TYPE == 'sqlite':
            cursor = connection.cursor()
            cursor.execute(f"""
                SELECT id, destination, start_date, end_date, description, 
                       highlights, photo_links, created_at, updated_at
                FROM journal_entries
                WHERE id = {placeholder}
            """, (entry_id,))
            row = cursor.fetchone()
            entry = dict(row) if row else None
        else:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(f"""
                SELECT id, destination, start_date, end_date, description, 
                       highlights, photo_links, created_at, updated_at
                FROM journal_entries
                WHERE id = {placeholder}
            """, (entry_id,))
            entry = cursor.fetchone()
        
        if not entry:
            return jsonify({'error': 'Entry not found'}), 404
        
        # Convert date objects to strings (MySQL only)
        if DB_TYPE == 'mysql':
            if entry.get('start_date'):
                entry['start_date'] = entry['start_date'].strftime('%Y-%m-%d') if hasattr(entry['start_date'], 'strftime') else entry['start_date']
            if entry.get('end_date'):
                entry['end_date'] = entry['end_date'].strftime('%Y-%m-%d') if hasattr(entry['end_date'], 'strftime') else entry['end_date']
            if entry.get('created_at'):
                entry['created_at'] = entry['created_at'].strftime('%Y-%m-%d %H:%M:%S') if hasattr(entry['created_at'], 'strftime') else entry['created_at']
            if entry.get('updated_at'):
                entry['updated_at'] = entry['updated_at'].strftime('%Y-%m-%d %H:%M:%S') if hasattr(entry['updated_at'], 'strftime') else entry['updated_at']
        
        return jsonify(entry), 200
    except Exception as e:
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
        placeholder = '?' if DB_TYPE == 'sqlite' else '%s'
        cursor = connection.cursor()
        query = f"""
            INSERT INTO journal_entries 
            (destination, start_date, end_date, description, highlights, photo_links)
            VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})
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
    except Exception as e:
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
        placeholder = '?' if DB_TYPE == 'sqlite' else '%s'
        cursor = connection.cursor()
        
        # Check if entry exists
        cursor.execute(f"SELECT id FROM journal_entries WHERE id = {placeholder}", (entry_id,))
        if not cursor.fetchone():
            return jsonify({'error': 'Entry not found'}), 404
        
        # Update entry
        query = f"""
            UPDATE journal_entries 
            SET destination = {placeholder}, start_date = {placeholder}, end_date = {placeholder}, 
                description = {placeholder}, highlights = {placeholder}, photo_links = {placeholder}
            WHERE id = {placeholder}
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
    except Exception as e:
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
        placeholder = '?' if DB_TYPE == 'sqlite' else '%s'
        cursor = connection.cursor()
        
        # Check if entry exists
        cursor.execute(f"SELECT id FROM journal_entries WHERE id = {placeholder}", (entry_id,))
        if not cursor.fetchone():
            return jsonify({'error': 'Entry not found'}), 404
        
        # Delete entry
        cursor.execute(f"DELETE FROM journal_entries WHERE id = {placeholder}", (entry_id,))
        connection.commit()
        
        return jsonify({'message': 'Entry deleted successfully'}), 200
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Failed to delete entry'}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    init_db()
    # Use environment variable to control debug mode (default to False for security)
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    # Get port from environment variable for cloud deployment (Railway, Heroku, etc.)
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
