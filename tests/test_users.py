def test_user_resource(client):
    # Test POST request to create a user
    user_data = {
        'name': 'Test User',
        'user_name': 'testuser',
        'email': 'test@example.com',
        'phone': '123456789',
        'password': 'test_password'
    }
    response = client.post('/users', json=user_data)
    assert response.status_code == 201
    assert response.json['message'] == 'User created'

    # Test GET request to retrieve all users
    response = client.get('/users')
    assert response.status_code == 200
    users = response.json
    assert isinstance(users, list)
    assert len(users) >= 1  # Assuming at least one user is created
    assert any(user['user_name'] == 'testuser' for user in users)

    # Test GET request to retrieve a specific user
    response = client.get('/users/testuser')
    assert response.status_code == 200
    user = response.json
    assert user['name'] == 'Test User'
    assert user['email'] == 'test@example.com'
    assert user['phone'] == '123456789'

    # Test PUT request to update a user
    updated_user_data = {
        'name': 'Updated Test User',
        'user_name': 'updatedtestuser',
        'email': 'updated_test@example.com',
        'phone': '987654321',
        'password': 'updated_test_password'
    }
    response = client.put('/users/testuser', json=updated_user_data)
    assert response.status_code == 200
    assert response.json['message'] == 'User updated'

    # Verify the user was updated
    response = client.get('/users/updatedtestuser')
    assert response.status_code == 200
    user = response.json
    assert user['name'] == 'Updated Test User'
    assert user['email'] == 'updated_test@example.com'
    assert user['phone'] == '987654321'

    # Test DELETE request to delete a user
    response = client.delete('/users/updatedtestuser')
    assert response.status_code == 200
    assert response.json['message'] == 'User deleted'

    # Verify the user was deleted
    response = client.get('/users/updatedtestuser')
    assert response.status_code == 404
    assert response.json['message'] == 'User not found'
