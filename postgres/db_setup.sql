-- 1. Users :
CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY ,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    UNIQUE (email)
);
-- 2. Restaurants :

CREATE TABLE Restaurants (
    restaurant_id SERIAL PRIMARY KEY ,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL
);
-- 3. Orders:

CREATE TABLE Orders (
    order_id SERIAL PRIMARY KEY ,
    user_id INT NOT NULL,
    restaurant_id INT NOT NULL,
    order_total DECIMAL(10,2) NOT NULL,
    delivery_status VARCHAR(20) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id)
);
-- 4. Drivers:

CREATE TABLE Drivers (
    driver_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    location VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE
);
-- 5. Payment:

CREATE TABLE Payment (
    payment_id SERIAL PRIMARY KEY,
    order_id INT NOT NULL,
    payment_method VARCHAR(20) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);

-- 6. Rating:
CREATE TABLE Rating (
    rating_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    restaurant_id INT NOT NULL,
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id)
);
-- 7. Address:

CREATE TABLE Address (
    address_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    state VARCHAR(255) NOT NULL,
    city  VARCHAR(255) NOT NULL,
    street VARCHAR(255) NOT NULL,
    pincode VARCHAR(255) NOT NULL,
    -- This FOREIGN KEY constraint ensures that data integrity is maintained
    -- what it does is: There can't be address without user_id that isn't inside USERS table
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);
-- 8. Menu:

CREATE TABLE Menu (
    menu_id SERIAL PRIMARY KEY,
    restaurant_id INT NOT NULL,
    menu_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id)
);

CREATE TABLE Dishes (
    dish_id SERIAL PRIMARY KEY,
    menu_id INT NOT NULL,
    dish_name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    ingredients VARCHAR(255) NOT NULL,
    FOREIGN KEY (menu_id) REFERENCES Menu(menu_id)
);

CREATE TABLE dish_additives (
    additive_id SERIAL PRIMARY KEY,
    dish_id INT NOT NULL,
    additive_name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (dish_id) REFERENCES Dishes(dish_id)
);
