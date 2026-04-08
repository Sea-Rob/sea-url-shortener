import pytest
import os

# Set testing environment variables BEFORE importing the app to ensure config picks them up
os.environ['FLASK_ENV'] = 'testing'
os.environ['API_KEY'] = 'test-secret-key'

from app import create_app
from app.models import db

@pytest.fixture
def app():
    app = create_app()
    from app.extensions import db, limiter
    with app.app_context():
        db.create_all()
        limiter.reset()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
