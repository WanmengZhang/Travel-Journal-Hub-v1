#!/bin/bash
# Start Travel Journal Hub
# Usage: ./start.sh [mysql|sqlite]
# Default: sqlite (easiest for development)

MODE=${1:-sqlite}

if [ "$MODE" = "mysql" ]; then
    echo "Starting Travel Journal Hub with MySQL..."
    
    # Start MySQL service if not running
    if ! sudo service mysql status > /dev/null 2>&1; then
        echo "Starting MySQL service..."
        sudo service mysql start
    fi

    # Set environment variables for MySQL
    export DB_HOST=localhost
    export DB_USER=root
    export DB_PASSWORD=password
    export DB_NAME=travel_journal
    export USE_SQLITE=false
    export FLASK_DEBUG=true
    
    echo "Using MySQL database"
else
    echo "Starting Travel Journal Hub with SQLite..."
    
    # Set environment variables for SQLite
    export USE_SQLITE=true
    export FLASK_DEBUG=false
    
    echo "Using SQLite database (no MySQL required)"
fi

echo ""
echo "Starting Flask application..."
python app.py
