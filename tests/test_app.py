import os
import sys
import pytest
from flask import url_for

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../flask_app')))

from app import app, db, Entry

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
    response = client.get('/restaurants')
    assert response.status_code == 200

def test_users_route(client):
    response = client.get('/users')
    assert response.status_code == 200

def test_add_entry(client):
    quantity_before_adding = len(Entry.query.all())
    response = client.get('/test_add')
    assert response.data == b'Added, check console for details'
    entries = Entry.query.all()
    assert len(entries) == quantity_before_adding + 1

def test_del_entry(client):
    db.session.add(Entry(name='test entry'))
    db.session.commit()
    quantity_before_deleting = len(Entry.query.all())
    response = client.get(f'/test_del/{quantity_before_deleting}')
    entries = Entry.query.all()
    assert len(entries) == quantity_before_deleting - 1
    

if __name__ == '__main__':
    pytest.main()

# pytest test_app.py