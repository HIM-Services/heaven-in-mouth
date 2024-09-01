import time


def test_restaurant_resource(client):
    # Test POST request to create a restaurant
    restaurant_data = {
        'name': 'Test Restaurant',
        'address': '221B Baker Street, London, NW1 6XE, UK',
        'phone': '987654321'
    }
    response = client.post('/restaurants', json=restaurant_data)
    assert response.status_code == 201

    # Wait a second between nominatim requests
    time.sleep(1)

    # Test GET request to retrieve all restaurants
    response = client.get('/restaurants')
    assert response.status_code == 200
    assert len(response.json) == 1  # Assuming only one restaurant is created
    restaurant_name = response.json[0]['name']
    restaurant_id = response.json[0]['restaurant_id']

    # Test if alias works correctly
    response = client.get(f'/restaurants/{restaurant_name}')
    assert response.status_code == 302
    assert response.location == f'/restaurants/{restaurant_id}'

    # Test GET request to retrieve a specific restaurant
    response = client.get(f'/restaurants/{restaurant_id}')
    assert response.status_code == 200
    assert response.json['name'] == 'Test Restaurant'
    assert response.json['address'] == '221B Baker Street, London, NW1 6XE, UK'
    assert response.json['phone'] == '987654321'

    # Test PUT request to update a restaurant
    updated_restaurant_data = {
        'name': 'Updated Test Restaurant',
        'address': '1 Infinite Loop, Cupertino, CA 95014',
        'phone': '123456789'
    }
    response = client.put(f'/restaurants/{restaurant_id}', json=updated_restaurant_data)
    assert response.json['message'] == 'Restaurant updated'
    assert response.status_code == 200

    # Test DELETE request to delete a restaurant
    response = client.delete(f'/restaurants/{restaurant_id}')
    assert response.json['message'] == 'Restaurant deleted'
    assert response.status_code == 200
    # Check if restaurant is deleted
    response = client.get('/restaurants')
    assert response.status_code == 200
    assert len(response.json) == 0
