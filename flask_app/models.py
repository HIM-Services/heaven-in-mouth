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

    def to_json(self):
        return {
            'id': self.user_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone
        }

    def __repr__(self):
        return f'<user {self.name}>'


class Restaurants(db.Model):
    __tablename__ = 'restaurants'
    # Changed id to the restaurant_id
    restaurant_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    menus = db.relationship('Menu', backref='restaurant',
                            cascade='all, delete-orphan', lazy=True)

    def to_json(self):
        return {
            'id': self.restaurant_id,
            'name': self.name,
            'address': self.address,
            'phone': self.phone
        }

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
    city = db.Column(db.String(255), nullable=False)
    street = db.Column(db.String(255), nullable=False)
    pincode = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Address {self.address_id}>'


class Menu(db.Model):
    __tablename__ = 'menu'
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey(
        'restaurants.restaurant_id'), nullable=False)
    # Nazwa pola dish_name
    menu_name = db.Column(db.String(255), nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'restaurant_id': self.restaurant_id,
            'menu_name': self.menu_name,
        }

    def __repr__(self):
        return f'<Menu {self.menu_name}>'


class Dishes(db.Model):
    __tablename__ = 'dishes'
    dish_id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False)
    dish_name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    ingredients = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Dish {self.dish_name}>'


class Dish_Additives(db.Model):
    __tablename__ = 'dish_additives'
    additive_id = db.Column(db.Integer, primary_key=True)
    dish_id = db.Column(db.Integer, db.ForeignKey(
        'dishes.dish_id'), nullable=False)
    additive_name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)

    def __repr__(self):
        return f'<Dish Additive {self.additive_name}>'