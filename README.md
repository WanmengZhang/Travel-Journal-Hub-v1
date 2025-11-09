# Travel Journal Hub

A multi-page web application for documenting and managing travel experiences. Built with Flask backend and vanilla JavaScript frontend, with MySQL database storage.

## Features

- **Homepage**: View a summary of recent travel entries with statistics
- **My Journals**: Browse all journal entries with search functionality
- **Entry Editor**: Create and edit journal entries with the following fields:
  - Destination (required)
  - Start and End dates (required)
  - Description
  - Highlights
  - Photo links (optional)

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Database**: MySQL or SQLite (automatic fallback)
- **API Communication**: Fetch API

## Prerequisites

- Python 3.7 or higher
- MySQL Server 5.7 or higher (optional - SQLite will be used automatically if MySQL is not available)
- pip (Python package manager)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/WanmengZhang/Travel-Journal-Hub-v1.git
   cd Travel-Journal-Hub-v1
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up database**
   
   **Option A: Use SQLite (Easiest - No Setup Required)**
   ```bash
   # Simply run the app - SQLite will be used automatically if MySQL is not available
   python app.py
   
   # Or explicitly enable SQLite mode:
   USE_SQLITE=true python app.py
   ```
   
   **Option B: Use MySQL (Recommended for Production)**
   
   Create a MySQL database or use environment variables to configure the database connection:
   
   ```bash
   export DB_HOST=localhost
   export DB_USER=root
   export DB_PASSWORD=your_password
   export DB_NAME=travel_journal
   ```
   
   Alternatively, you can modify the database configuration in `app.py`.

4. **Run the application**
   ```bash
   python app.py
   ```
   
   **Quick Start (Recommended for Development):**
   ```bash
   # Use the provided start script (automatically uses SQLite)
   ./start.sh
   
   # Or manually with SQLite:
   USE_SQLITE=true python app.py
   
   # Or with MySQL (requires MySQL server running):
   ./start.sh mysql
   ```
   
   The application will:
   - Automatically detect and use MySQL if available, otherwise fall back to SQLite
   - Initialize the database and create necessary tables
   - Start the Flask server on http://localhost:5000

## Usage

1. **Access the application**
   - Open your web browser and navigate to `http://localhost:5000`

2. **Create a new entry**
   - Click "New Entry" in the navigation or "Create New Entry" button
   - Fill in the required fields (destination, start date, end date)
   - Optionally add description, highlights, and photo links
   - Click "Save Entry"

3. **View all journals**
   - Navigate to "My Journals" to see all your entries
   - Use the search bar to filter entries by destination, description, or highlights

4. **Edit or delete entries**
   - From "My Journals" page, click "Edit" to modify an entry
   - Click "Delete" to remove an entry (confirmation required)

## Project Structure

```
Travel-Journal-Hub-v1/
├── app.py                 # Flask backend application
├── requirements.txt       # Python dependencies
├── templates/             # HTML templates
│   ├── index.html        # Homepage
│   ├── journals.html     # My Journals page
│   └── editor.html       # Entry editor page
└── static/               # Static files
    ├── styles.css        # Application styles
    ├── home.js           # Homepage JavaScript
    ├── journals.js       # Journals page JavaScript
    └── editor.js         # Editor page JavaScript
```

## API Endpoints

- `GET /api/entries` - Retrieve all journal entries
- `GET /api/entries/<id>` - Retrieve a specific entry
- `POST /api/entries` - Create a new entry
- `PUT /api/entries/<id>` - Update an existing entry
- `DELETE /api/entries/<id>` - Delete an entry

## Database Schema

**journal_entries** table:
- `id` (INT, Primary Key, Auto Increment)
- `destination` (VARCHAR(255), NOT NULL)
- `start_date` (DATE, NOT NULL)
- `end_date` (DATE, NOT NULL)
- `description` (TEXT)
- `highlights` (TEXT)
- `photo_links` (TEXT)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

## Development

### Running with SQLite (Development Mode)
For quick local development without MySQL:

```bash
USE_SQLITE=true python app.py
```

This creates a local `travel_journal.db` file in the project directory.

### Running with MySQL (Production Mode)
To run the application in development mode with debug enabled:

```bash
export FLASK_DEBUG=true
python app.py
```

The Flask development server will run on `http://localhost:5000` with auto-reload enabled.

### Running Tests
To verify your installation and test the application:

```bash
python test_app.py
```

This will check:
- All required Python modules are installed correctly
- Database driver availability (MySQL and/or SQLite)
- Flask app structure and routes
- Template and static file existence

## Environment Variables

The application supports the following environment variables for configuration:

| Variable | Default | Description |
|----------|---------|-------------|
| `USE_SQLITE` | `false` | Force SQLite mode (set to `true`) |
| `SQLITE_DB_PATH` | `travel_journal.db` | SQLite database file location |
| `DB_HOST` | `localhost` | MySQL server hostname |
| `DB_USER` | `root` | MySQL username |
| `DB_PASSWORD` | `` | MySQL password |
| `DB_NAME` | `travel_journal` | MySQL database name |
| `FLASK_DEBUG` | `false` | Enable Flask debug mode (set to `true`) |

## License

This project is open source and available for educational purposes.