## Travel-Journal-Hub — Copilot instructions for code changes

Purpose: give AI coding agents the concrete, repo-specific knowledge needed to be productive immediately.

- Project type: small Flask monolith (single `app.py`) with a vanilla JS frontend in `static/` and server-rendered pages in `templates/`.
- Key runtime pieces: `app.py` serves three HTML pages (`/`, `/journals`, `/editor`) and a REST API under `/api/entries` (GET/POST/PUT/DELETE).

What to know before editing code
- Database: MySQL. Connection config lives in the `DB_CONFIG` dict in `app.py` and is overridden by env vars: `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`.
  - `init_db()` in `app.py` will create the database and the `journal_entries` table if missing. Avoid running this on production-like data without backups.
- JSON API conventions: `app.py` returns JSON for API routes and converts date/datetime objects to ISO-like strings before returning (see `get_entries()` and `get_entry()`). Follow the same conversion pattern when adding fields.
- Frontend wiring: client code in `static/*.js` uses the Fetch API to call the `/api/entries` endpoints and expects the date strings described above. If you change request/response shapes, update `static/editor.js` and `static/journals.js` accordingly.

Developer workflows & commands
- Install: `pip install -r requirements.txt` (see `README.md`).
- Run app locally: `python app.py`. Control debug mode with `FLASK_DEBUG=true` (default is False). App binds to `0.0.0.0:5000`.
- Lightweight tests: run `python test_app.py` — this checks imports, presence of templates and static files, and basic app structure. Note: it imports `app` which may attempt DB connection; prefer setting DB env vars or mocking when running CI.

Project-specific conventions and patterns
- Single-file backend: most server logic is in `app.py`. Keep routes, DB access, and simple validation there unless creating a larger refactor.
- DB migration pattern: there is no migration tool. If you add new columns, update `init_db()` to create them (or provide SQL migration steps) and update all INSERT/UPDATE queries in `app.py`.
- Error handling: routes return JSON `{'error': 'message'}` with appropriate HTTP codes. Preserve this pattern when adding new API errors.
- Date handling: store dates as `DATE` in DB; when returning JSON, call `.strftime('%Y-%m-%d')` for `start_date`/`end_date` and `%Y-%m-%d %H:%M:%S` for timestamps.

Examples of common tasks (concrete)
- Add a new entry field `mood` (string):
  1. Add `mood VARCHAR(50)` to the `CREATE TABLE` SQL in `init_db()`.
  2. Update the `INSERT` query in `create_entry()` to include `mood` and pull from `data.get('mood','')`.
  3. Update `UPDATE` query in `update_entry()` similarly.
  4. Update `static/editor.js` to send `mood` in the JSON body when saving.
  5. Update any UI templates (`templates/*.html`) to render the new field where appropriate.

Files to inspect when making changes
- Backend: `app.py` (routes, DB logic, `init_db`, `DB_CONFIG`)
- Frontend: `static/editor.js`, `static/journals.js`, `static/home.js` (fetch usage)
- Templates: `templates/index.html`, `templates/journals.html`, `templates/editor.html`
- Tests: `test_app.py` (simple sanity checks used by maintainers)
- Docs: `README.md` (install/run instructions and high-level architecture)

Notes and gotchas
- The repo assumes a MySQL server is reachable. For local dev, set DB env vars; otherwise some endpoints will return DB connection errors.
- There is no ORM — raw SQL and `mysql.connector` are used. Watch out for SQL injection when constructing queries; the code uses parameterized queries (use `%s` placeholders) — follow the same pattern.
- Keep JSON shapes stable: clients expect fields named exactly as used today (e.g., `start_date`, `end_date`, `photo_links`).

If anything in this file is unclear or you'd like more examples (e.g., adding migrations, wiring CI, or refactoring the DB layer), tell me what area to expand and I will iterate.

