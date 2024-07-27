import time


# Sample test data
restaurant_data = {
    'name': 'Test Restaurant',
    'address': '350 5th Ave, New York, NY 10118, USA',
    'phone': '987654321'
}

menu_data = {
    'menu_name': 'Test Menu'
}

dish_data = {
    'dish_name': 'Test Dish',
    'price': 10.99,
    'ingredients': 'Test Ingredients'
}

additive_data = {
    'additive_name': 'Test Additive',
    'price': 1.99
}


def test_all_resources(client):
    # Test POST request to create a restaurant
    response = client.post('/restaurants', json=restaurant_data)
    assert response.status_code == 201

    # Wait a second between nominatim requests
    time.sleep(1)

    # Test POST request to create a menu
    response = client.post('/restaurants/1/menu', json=menu_data)
    assert response.status_code == 201
    assert response.json['message'] == 'Menu created'

    # Test GET request to retrieve the menu
    response = client.get('/menu/1')
    assert response.status_code == 200
    assert response.json['menu_id'] == 1
    assert response.json['menu_name'] == 'Test Menu'

    # Test POST request to create a dish
    response = client.post('/menu/1/dishes', json=dish_data)
    assert response.status_code == 201
    assert response.json['message'] == 'Dish created'

    # Test GET request to retrieve the dish
    response = client.get('/dishes/1')
    assert response.status_code == 200
    assert response.json['dish_name'] == 'Test Dish'
    assert response.json['price'] == 10.99
    assert response.json['ingredients'] == 'Test Ingredients'

    # Test POST request to create a dish additive
    response = client.post('/dishes/1/additives', json=additive_data)
    assert response.status_code == 201
    assert response.json['message'] == 'Additive created'

    # Test GET request to retrieve the dish additive
    response = client.get('/additives/1')
    assert response.status_code == 200
    assert response.json['additive_name'] == 'Test Additive'
    assert response.json['price'] == 1.99

    # Test PUT request to update the menu
    updated_menu_data = {
        'menu_name': 'Updated Test Menu'
    }
    response = client.put('/menu/1', json=updated_menu_data)
    assert response.status_code == 200
    assert response.json['message'] == 'Menu updated'

    # Retrieve the updated menu
    response = client.get('/menu/1')
    assert response.status_code == 200
    assert response.json['menu_name'] == 'Updated Test Menu'

    # Test PUT request to update the dish
    updated_dish_data = {
        'dish_name': 'Updated Test Dish',
        'price': 12.99,
        'ingredients': 'Updated Ingredients'
    }
    response = client.put('/dishes/1', json=updated_dish_data)
    assert response.status_code == 200
    assert response.json['message'] == 'Dish updated'

    # Retrieve the updated dish
    response = client.get('/dishes/1')
    assert response.status_code == 200
    assert response.json['dish_name'] == 'Updated Test Dish'
    assert response.json['price'] == 12.99
    assert response.json['ingredients'] == 'Updated Ingredients'

    # Test PUT request to update the dish additive
    updated_additive_data = {
        'additive_name': 'Updated Test Additive',
        'price': 2.99
    }
    response = client.put('/additives/1', json=updated_additive_data)
    assert response.status_code == 200
    assert response.json['message'] == 'Additive updated'

    # Retrieve the updated additive
    response = client.get('/additives/1')
    assert response.status_code == 200
    assert response.json['additive_name'] == 'Updated Test Additive'
    assert response.json['price'] == 2.99

    # Test DELETE request to delete the dish additive
    response = client.delete('/additives/1')
    assert response.status_code == 200
    assert response.json['message'] == 'Additive deleted'

    # Verify the additive is deleted
    response = client.get('/additives/1')
    assert response.status_code == 404

    # Test DELETE request to delete the dish
    response = client.delete('/dishes/1')
    assert response.status_code == 200
    assert response.json['message'] == 'Dish deleted'

    # Verify the dish is deleted
    response = client.get('/dishes/1')
    assert response.status_code == 404

    # Test DELETE request to delete the menu
    response = client.delete('/menu/1')
    assert response.status_code == 200
    assert response.json['message'] == 'Menu deleted'

    # Verify the menu is deleted
    response = client.get('/menu/1')
    assert response.status_code == 404
