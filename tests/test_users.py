def test_user_resource(client):
    # Test POST request to create a user
    user_data = {
        'name': 'Test User',
        'user_name' : 'test_user',
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

    # Test GET request to retrieve a specific user by user_name
    user_name = response.json[0]['user_name']
    response = client.get(f'/users/{user_name}')
    assert response.status_code == 302
    assert response.json['name'] == 'Test User'
    assert response.json['user_name'] == 'test_user'
    assert response.json['email'] == 'test@example.com'
    assert response.json['phone'] == '123456789'

    # Test GET request to retrieve a specific user
    user_id = response.json[0]['user_id']
    response = client.get(f'/users/{user_id}')
    assert response.status_code == 200
    assert response.json['name'] == 'Test User'
    assert response.json['user_name'] == 'test_user'
    assert response.json['email'] == 'test@example.com'
    assert response.json['phone'] == '123456789'

    # Test PUT request to update a user
    updated_user_data = {
        'name': 'Updated Test User',
        'email': 'updated_test@example.com',
        'user_name': 'updated_test_user',
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


    
