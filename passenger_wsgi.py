import sys
import os

# 1. Configuration: Path to your virtual environment's site-packages
# Change this path to correctly point to your venv if it is located elsewhere.
VENV_PATH = os.path.join(os.getcwd(), 'venv', 'lib', 'python3.10', 'site-packages')
# Note: Ensure the python version above (e.g., 3.10) matches your environment.
if os.path.exists(VENV_PATH):
    sys.path.insert(0, VENV_PATH)

# Add the current directory (project root) to sys.path
sys.path.insert(0, os.getcwd())

# 2. Import the Flask application factory
from app import create_app

application = create_app()
