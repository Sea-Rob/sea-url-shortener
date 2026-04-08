#!/bin/bash

# Configuration
TEST_DB="test_run.db"
API_KEY_VAL="test-api-key-123"

# 1. Initialize venv if it doesn't exist
if [ ! -d "venv" ]; then
    echo "--- Creating virtual environment ---"
    python -m venv venv
fi

# 2. Activate venv and install dependencies
source venv/bin/activate
echo "--- Installing requirements ---"
pip install -r requirements.txt

# 3. Environment Variables
export FLASK_APP=app.py
export FLASK_ENV=testing
export API_KEY=$API_KEY_VAL
export TEST_DATABASE_URI="sqlite:///$TEST_DB"

# 4. Initialize the database
echo "--- Initializing database ---"
if [ -f "$TEST_DB" ]; then
    rm "$TEST_DB"
fi
flask setup init-db

# 5. Start the Flask app in background
echo "--- Starting Flask app in background ---"
flask run --port=5000 > flask_test.log 2>&1 &
FLASK_PID=$!

# Give it a bit of time to start
sleep 2

# 6. Test the /shorten endpoint with curl
echo "--- Testing /shorten endpoint ---"
RESPONSE=$(curl -s -X POST http://127.0.0.1:5000/shorten \
     -H "Authorization: Bearer $API_KEY_VAL" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.google.com"}')

echo "Response from API: $RESPONSE"

# Verify response
if [[ "$RESPONSE" == *"short_id"* ]]; then
    echo "SUCCESS: Check /shorten test passed!"
    SHORT_ID=$(echo $RESPONSE | sed -E 's/.*"short_id":"([^"]+)".*/\1/')
    echo "Short ID generated: $SHORT_ID"
else
    echo "FAILURE: /shorten test failed!"
    cat flask_test.log
fi

# 7. Cleanup
echo "--- Cleaning up ---"
kill $FLASK_PID
rm "$TEST_DB"
echo "--- Test Script Completed ---"
