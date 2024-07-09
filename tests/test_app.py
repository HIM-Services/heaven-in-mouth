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
    assert response.is_json 
    restaurants = response.json.get('restaurants')
    assert restaurants is not None
    assert len(restaurants) == 0

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

    response = client.get('/rest')
    assert response.status_code == 200
    assert response.is_json
    restaurants = response.json.get('restaurants')
    assert restaurants is not None
    assert len(restaurants) == 1
    assert restaurants[0]['name'] == 'Test Restaurant'
    assert restaurants[0]['address'] == 'Test Street'
    assert restaurants[0]['phone'] == '123456789'

def test_rest_add_invalid_post(client):
    # Invalid input test
    data = {
        # No restaurant name
        'address': 'Test Street',
        'phone': '123456789'
    }
    response = client.post('/rest_add', data=data, follow_redirects=True)
    assert response.status_code == 400
    response = client.get('/rest')
    assert response.status_code == 200
    assert response.is_json
    restaurants = response.json.get('restaurants')
    assert restaurants is not None
    assert len(restaurants) == 0
    
def test_menu_add_post(client):
    data_restaurant = {
        'name': 'Menu Test Restaurant',
        'address': 'Test Street',
        'phone': '123456789'
    }
    response = client.post('/rest_add', data=data_restaurant, follow_redirects=True)
    assert response.status_code == 200

    # Adding a dish to menu
    data_menu = {
        'dish_name': 'Test Dish',
        'price': '15.99'
    }
    restaurant_id = Restaurant.query.filter_by(name="Menu Test Restaurant").first_or_404().id
    response = client.post(f'/menu_add/{restaurant_id}', data=data_menu, follow_redirects=True)
    assert response.status_code == 200

    # Check if the menu item is added correctly
    response = client.get('/menu')
    assert response.status_code == 200
    assert response.is_json
    menu_items = response.json.get('menu_items')
    assert menu_items is not None
    assert len(menu_items) == 1
    assert menu_items[0]['dish_name'] == 'Test Dish'
    assert menu_items[0]['price'] == 15.99

if __name__ == '__main__':
    pytest.main()

# pytest test_app.py