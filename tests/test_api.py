import os
import sys
import pytest

# Ensure the 'flask_app' directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../flask_app')))

from api import app, db


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


# Test UserResource
def test_user_resource(client):
    # Test POST request to create a user
    user_data = {
        'name': 'Test User',
        'email': 'test@example.com',
        'phone': '123456789',
        'password': 'test_password'
    }
    response = client.post('/users', json=user_data)
    assert response.status_code == 201

    # Test GET request to retrieve all users
    response = client.get('/users')
    assert response.status_code == 200
    assert len(response.json) == 1  # Assuming only one user is created

    # Test GET request to retrieve a specific user
    user_id = response.json[0]['id']
    response = client.get(f'/users/{user_id}')
    assert response.status_code == 200
    assert response.json['name'] == 'Test User'
    assert response.json['email'] == 'test@example.com'
    assert response.json['phone'] == '123456789'

    # Test PUT request to update a user
    updated_user_data = {
        'name': 'Updated Test User',
        'email': 'updated_test@example.com',
        'phone': '987654321',
        'password': 'updated_test_password'
    }
    response = client.put(f'/users/{user_id}', json=updated_user_data)
    assert response.json['message'] == 'User updated'
    assert response.status_code == 200

    # Test DELETE request to delete a user
    response = client.delete(f'/users/{user_id}')
    assert response.json['message'] == 'User deleted'
    assert response.status_code == 200


# Test RestaurantResource
def test_restaurant_resource(client):
    # Test POST request to create a restaurant
    restaurant_data = {
        'name': 'Test Restaurant',
        'address': 'Test Address',
        'phone': '987654321'
    }
    response = client.post('/restaurants', json=restaurant_data)
    assert response.status_code == 201

    # Test GET request to retrieve all restaurants
    response = client.get('/restaurants')
    assert response.status_code == 200
    assert len(response.json) == 1  # Assuming only one restaurant is created

    # Test GET request to retrieve a specific restaurant
    restaurant_id = response.json[0]['id']
    response = client.get(f'/restaurants/{restaurant_id}')
    assert response.status_code == 200
    assert response.json['name'] == 'Test Restaurant'
    assert response.json['address'] == 'Test Address'
    assert response.json['phone'] == '987654321'

    # Test PUT request to update a restaurant
    updated_restaurant_data = {
        'name': 'Updated Test Restaurant',
        'address': 'Updated Test Address',
        'phone': '123456789'
    }
    response = client.put(f'/restaurants/{restaurant_id}', json=updated_restaurant_data)
    assert response.json['message'] == 'Restaurant updated'
    assert response.status_code == 200

    # Test DELETE request to delete a restaurant
    response = client.delete(f'/restaurants/{restaurant_id}')
    assert response.json['message'] == 'Restaurant deleted'
    assert response.status_code == 200


if __name__ == '__main__':
    pytest.main()
