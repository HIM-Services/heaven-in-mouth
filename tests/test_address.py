import time


def test_address_resource(client):
    # Test POST request to create a user
    user_data = {
        'name': 'Test User',
        'email': 'test@example.com',
        'phone': '123456789',
        'password': 'test_password'
    }
    response = client.post('/users', json=user_data)
    assert response.status_code == 201
    user_id = 1
    address_data = {
        'state': 'Mazowieckie',
        'city': 'Warszawa',
        'street': 'Wspólna 15',
        'pincode': '05-075'
    }
    response = client.post(f'/users/{user_id}/address', json=address_data)

    # Wait a second between nominatim requests
    time.sleep(1)

    assert response.status_code == 201

    # Test GET request to retrieve a specific address
    address_id = 1
    response = client.get(f'/address/{address_id}')
    assert response.status_code == 200
    assert response.json['state'] == 'Mazowieckie'
    assert response.json['city'] == 'Warszawa'
    assert response.json['street'] == 'Wspólna 15'
    assert response.json['pincode'] == '05-075'
    assert round(response.json['longitude'], 6) == 21.189461
    assert round(response.json['latitude'], 6) == 52.247469

    # Test PUT request to update an address
    updated_address_data = {
        'state': 'Mazowieckie',
        'city': 'Warszawa',
        'street': 'Wspólna 16',
        'pincode': '05-075'
    }
    response = client.put(f'/address/{address_id}', json=updated_address_data)

    # Wait a second between nominatim requests
    time.sleep(1)

    assert response.status_code == 200
    assert response.json['message'] == 'Address updated'

    response = client.get(f'/address/{address_id}')
    assert response.status_code == 200
    assert response.json['state'] == 'Mazowieckie'
    assert response.json['city'] == 'Warszawa'
    assert response.json['street'] == 'Wspólna 16'
    assert response.json['pincode'] == '05-075'
    assert round(response.json['longitude'], 6) == 21.186653
    assert round(response.json['latitude'], 6) == 52.24638

    # Test DELETE request to delete an address
    response = client.delete(f'/address/{address_id}')
    assert response.json['message'] == 'Address deleted'
    assert response.status_code == 200

    # Check if address is deleted
    response = client.get(f'/address/{address_id}')
    assert response.status_code == 404
