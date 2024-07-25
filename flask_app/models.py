from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    admin = db.Column(db.Boolean, default=False)
    address = db.relationship('Address', backref='user', uselist=False, cascade='all, delete-orphan')

    def to_json(self):
        data = {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone
        }
        if self.address:
            data['address'] = self.address.to_json()
        return data

    def __repr__(self):
        return f'<user {self.name}>'


class Restaurants(db.Model):
    __tablename__ = 'restaurants'
    # Changed id to the restaurant_id
    restaurant_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    menus = db.relationship('Menu', backref='restaurants',
                            cascade='all, delete-orphan', lazy=True)

    def to_json(self, include_menu=False):
        data = {
            'restaurant_id': self.restaurant_id,
            'name': self.name,
            'address': self.address,
            'phone': self.phone,
            'longitude': self.longitude,
            'latitude': self.latitude
        }
        if include_menu:
            data['menus'] = [menu.to_json() for menu in self.menus]
        return data

    def __repr__(self):
        return f'<Restaurant {self.name}>'


class Orders(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey(
        'restaurants.restaurant_id'), nullable=False)
    order_total = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    delievery_status = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Order {self.order_id}>'


class Drivers(db.Model):
    __tablename__ = 'drivers'
    driver_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)

    def __repr__(self):
        return f'<Driver {self.name}>'


class Payment(db.Model):
    __tablename__ = 'payment'
    payment_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.order_id'), nullable=False)
    payment_method = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    status = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Payment {self.payment_id}>'


class Rating(db.Model):
    __tablename__ = 'rating'
    rating_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey(
        'restaurants.restaurant_id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Rating {self.rating_id}>'


class Address(db.Model):
    __tablename__ = 'address'
    address_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    street = db.Column(db.String(255), nullable=False)
    pincode = db.Column(db.String(255), nullable=False)
    # longitude and latitude are used to calculate the distance between restaurant and customer
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)

    def to_json(self):
        return {
            'address_id': self.address_id,
            'user_id': self.user_id,
            'state': self.state,
            'city': self.city,
            'street': self.street,
            'pincode': self.pincode,
            'longitude': self.longitude,
            'latitude': self.latitude
        }

    def __repr__(self):
        return f'<Address {self.address_id}>'


class Menu(db.Model):
    __tablename__ = 'menu'
    menu_id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey(
        'restaurants.restaurant_id'), nullable=False)
    menu_name = db.Column(db.String(255), nullable=False)
    dishes = db.relationship('Dishes', backref='menu', cascade='all, delete-orphan', lazy=True)

    def to_json(self):
        return {
            'menu_id': self.menu_id,
            'restaurant_id': self.restaurant_id,
            'menu_name': self.menu_name,
            'dishes': [dish.to_json() for dish in self.dishes]
        }

    def __repr__(self):
        return f'<Menu {self.menu_name}>'


class Dishes(db.Model):
    __tablename__ = 'dishes'
    dish_id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.menu_id'), nullable=False)
    dish_name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    ingredients = db.Column(db.String(255), nullable=False)
    additives = db.relationship('Dish_Additives', backref='dishes', cascade='all, delete-orphan', lazy=True)

    def to_json(self, include_additives=False):
        return {
            'dish_id': self.dish_id,
            'menu_id': self.menu_id,
            'dish_name': self.dish_name,
            'price': float(self.price),
            'ingredients': self.ingredients,
            'additives': [additive.to_json() for additive in self.additives]
        }

    def __repr__(self):
        return f'<Dish {self.dish_name}>'


class Dish_Additives(db.Model):
    __tablename__ = 'dish_additives'
    additive_id = db.Column(db.Integer, primary_key=True)
    dish_id = db.Column(db.Integer, db.ForeignKey(
        'dishes.dish_id'), nullable=False)
    additive_name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)

    def to_json(self):
        return {
            'additive_id': self.additive_id,
            'dish_id': self.dish_id,
            'additive_name': self.additive_name,
            'price': float(self.price)
        }

    def __repr__(self):
        return f'<Dish Additive {self.additive_name}>'
