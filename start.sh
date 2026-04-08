#!/bin/bash

# Configuration
export FLASK_APP=app.py
export FLASK_ENV=testing
export API_KEY=apitestkey
export TEST_DATABASE_URI="sqlite:///testing.db"

# 1. Activate venv if it exists
if [ -d "venv" ]; then
    echo "--- Activating virtual environment ---"
    source venv/bin/activate
else
    echo "--- [Warning] venv not found. Ensure dependencies are installed. ---"
fi

# 2. Automatically initialize the testing database if it doesn't exist
if [ ! -f "testing.db" ]; then
    echo "--- First run: Initializing testing database ---"
    flask setup init-db
fi

# 3. Start the Flask server
echo "--- Starting Sea URL Shortener (TESTING MODE) ---"
echo "API_KEY is set to: $API_KEY"
echo "Database: $TEST_DATABASE_URI"
flask run --host=0.0.0.0 --port=5000
