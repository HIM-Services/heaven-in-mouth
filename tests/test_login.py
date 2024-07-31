def test_login(client):
    # Create a user for login test
    user_data = {
        'name': 'Login Test User',
        'user_name': 'test_user',
        'email': 'login_test@example.com',
        'phone': '123456789',
        'password': 'test_password'
    }
    client.post('/users', json=user_data)

    login_data = {
        'email': 'non_existing@example.com',
        'password': 'test_password'
    }

    # Test login with non-existing email
    response = client.post('/login', json=login_data)
    assert response.status_code == 404
    assert response.json['message'] == 'User not found'

    # Test login with incorrect password
    login_data['email'] = 'login_test@example.com'
    login_data['password'] = 'incorrect_password'
    response = client.post('/login', json=login_data)
    assert response.status_code == 401
    assert response.json['message'] == 'Incorrect password'

    # Test login with correct credentials
    login_data['password'] = 'test_password'
    response = client.post('/login', json=login_data)
    assert response.status_code == 200
    assert response.json['message'] == 'Logged in successfully'

    # Test if user is logged in
    response = client.get('/login')
    assert response.status_code == 200
    assert response.json['message'] == 'User is logged in'

    # Log out the user
    response = client.get('/logout')
    assert response.status_code == 200
    assert response.json['message'] == 'Logged out successfully'

    # Test if user is logged out
    response = client.get('/login')
    assert response.status_code == 401
    assert response.json['message'] == 'User is not logged in'
