import os
import sys
import pytest
from flask import url_for

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../flask_app')))

from app import app, db, Restaurant

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TEST_DATABASE_URL', app.config['SQLALCHEMY_DATABASE_URI'])
    with app.app_context():
        # set up the database
        db.create_all()
        yield app.test_client()
        # clean up database after test
        db.session.remove()
        db.drop_all()

def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200

def test_restaurants_route(client):
    response = client.get('/rest')
    assert response.status_code == 200

def test_users_route(client):
    response = client.get('/users')
    assert response.status_code == 200

def test_rest_add_post(client):
    data = {
        'name': 'Test Restaurant',
        'address': 'Test Street',
        'phone': '123456789'
    }
    response = client.post('/rest_add', data=data, follow_redirects=True)
    assert response.status_code == 200

    #check if this restaurant is shown on restaurant route
    response = client.get('/rest')
    assert response.status_code == 200
    assert b'Test Restaurant' in response.data
    assert b'Test Street' in response.data
    assert b'123456789' in response.data

def test_rest_add_invalid_post(client):
    #test bad input
    data = {
        # No restaurant name
        'address': 'Test Street',
        'phone': '123456789'
    }
    response = client.post('/rest_add', data=data, follow_redirects=True)
    assert response.status_code == 400
    

if __name__ == '__main__':
    pytest.main()

# pytest test_app.py