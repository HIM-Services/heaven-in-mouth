import os
import sys
import pytest

# Ensure the 'flask_app' directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../flask_app')))

from api import app, db


# This file allows sharing fixtures across multiple tests
@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TEST_DATABASE_URL', app.config['SQLALCHEMY_DATABASE_URI'])
    with app.app_context():
        # Set up the database
        db.create_all()
        yield app.test_client()
        # Clean up database after test
        db.session.remove()
        db.drop_all()
