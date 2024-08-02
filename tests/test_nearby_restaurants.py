import pytest
from flask import json
from models import db, Users, Address, Restaurants
from api import app

@pytest.fixture
def setup_test_data():
    with app.app_context():
        # Add test user
        user = Users(
            user_id=1,
            name='Test User',
            email='testuser@example.com',
            password='password',
            phone='1234567890'
        )
        db.session.add(user)
        db.session.commit()

        # Add test address for the user
        user_address = Address(
            user_id=1,
            state='CA',
            city='Mountain View',
            street='1600 Amphitheatre Parkway',
            pincode='94043',
            longitude=21.0122287,
            latitude=52.2296756
        )
        user_address.set_geolocation()
        
        db.session.add(user_address)

        # Add test restaurants
        restaurant_within_range = Restaurants(
            restaurant_id=1,
            name='Nearby Restaurant',
            address='1234 Nearby St',
            phone='1234567890',
            longitude=21.020000,
            latitude=52.230000
        )
        restaurant_within_range.set_geolocation()
        
        restaurant_out_of_range = Restaurants(
            restaurant_id=2,
            name='Far Restaurant',
            address='5678 Far St',
            phone='0987654321',
            longitude=20.500000,
            latitude=51.500000
        )
        restaurant_out_of_range.set_geolocation()
        
        db.session.add(restaurant_within_range)
        db.session.add(restaurant_out_of_range)
        db.session.commit()

        yield


def test_nearby_restaurants(client, setup_test_data):
    # Make a GET request to the '/users/1/nearby' endpoint
    response = client.get('/users/1/nearby')
    assert response.status_code == 200

    data = json.loads(response.data)
    
    # Check if the restaurant within range is returned
    assert any(restaurant['name'] == 'Nearby Restaurant' for restaurant in data)
    
    # Check if the restaurant out of range is not returned
    assert not any(restaurant['name'] == 'Far Restaurant' for restaurant in data)