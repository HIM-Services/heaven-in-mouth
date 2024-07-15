from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse, abort
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
from models import db, Users, Restaurants, Menu
import os


# read database credentials from enviroment
def get_env_variable(name):
    try:
        return os.getenv(name)
    except KeyError:
        message = f"Expected environment variable '{name}' not set."
        raise Exception(message)


# dotenv is used to read the .env file and set the environment variables
load_dotenv()

SECRET_KEY = get_env_variable("SECRET_KEY")
POSTGRES_URL = get_env_variable("POSTGRES_URL")
POSTGRES_USER = get_env_variable("POSTGRES_USER")
POSTGRES_PW = get_env_variable("POSTGRES_PW")
POSTGRES_DB = get_env_variable("POSTGRES_DB")


DB_URL = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PW}@{POSTGRES_URL}/{POSTGRES_DB}'  # noqa F405


# SECRET KEY is used to sign the session cookie and other security related stuff #
app = Flask(__name__)
api = Api(app)
app.secret_key = 'secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# db is initialized in models.py file and imported using *
db.init_app(app)  # noqa F405


# Parsers that check if the request has the required fields (* will be moved to other file soon *)
user_parser = reqparse.RequestParser()
user_parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")
user_parser.add_argument('email', type=str, required=True, help="Email cannot be blank!")
user_parser.add_argument('phone', type=str, required=True, help="Phone cannot be blank!")
user_parser.add_argument('password', type=str, required=True, help="Password cannot be blank!")

restaurant_parser = reqparse.RequestParser()
restaurant_parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")
restaurant_parser.add_argument('address', type=str, required=True, help="Address cannot be blank!")
restaurant_parser.add_argument('phone', type=str, required=True, help="Phone cannot be blank!")

menu_parser = reqparse.RequestParser()
menu_parser.add_argument('menu_name', type=str, required=True, help="Menu name cannot be blank!")
menu_parser.add_argument('price', type=float, required=True, help="Price cannot be blank!")


# Define Resources
class UserResource(Resource):
    # Get all users or a specific user
    def get(self, user_id=None):
        if user_id:
            user = db.session.get(Users, user_id)
            if not user:
                abort(404, message='User not found')

            return jsonify(user.to_json())
        else:
            users = Users.query.all()
            return jsonify([user.to_json() for user in users])

    # Create a new user
    def post(self):
        args = user_parser.parse_args()
        name = args['name']
        email = args['email']
        phone = args['phone']
        password = generate_password_hash(args['password'])
        new_user = Users(name=name, email=email, phone=phone, password=password)
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User created'}, 201

    # Update a user
    def put(self, user_id):
        user = db.session.get(Users, user_id)
        if not user:
            abort(404, message='User not found')

        args = user_parser.parse_args()
        user.name = args['name']
        user.email = args['email']
        user.phone = args['phone']
        user.password = generate_password_hash(args['password'])
        db.session.commit()
        return {'message': 'User updated'}

    # Delete a user
    def delete(self, user_id):
        user = db.session.get(Users, user_id)
        if not user:
            abort(404, message='User not found')

        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted'}


class RestaurantResource(Resource):
    # Get all restaurants or a specific restaurant
    def get(self, restaurant_id=None):
        if restaurant_id:
            restaurant = db.session.get(Restaurants, restaurant_id)
            if not restaurant:
                abort(404, message='Restaurant not found')

            return jsonify(restaurant.to_json())
        else:
            restaurants = Restaurants.query.all()
            return jsonify([restaurant.to_json() for restaurant in restaurants])

    # Create a new restaurant
    def post(self):
        args = restaurant_parser.parse_args()
        new_restaurant = Restaurants(
            name=args['name'],
            address=args['address'],
            phone=args['phone']
        )
        db.session.add(new_restaurant)
        db.session.commit()
        return {'message': 'Restaurant created'}, 201

    # Update a restaurant
    def put(self, restaurant_id):
        restaurant = db.session.get(Restaurants, restaurant_id)
        if not restaurant:
            abort(404, message='Restaurant not found')

        args = restaurant_parser.parse_args()
        restaurant.name = args['name']
        restaurant.address = args['address']
        restaurant.phone = args['phone']
        db.session.commit()
        return {'message': 'Restaurant updated'}

    # Delete a restaurant
    def delete(self, restaurant_id):
        restaurant = db.session.get(Restaurants, restaurant_id)
        if not restaurant:
            abort(404, message='Restaurant not found')

        db.session.delete(restaurant)
        db.session.commit()
        return {'message': 'Restaurant deleted'}


class MenuResource(Resource):
    def get(self, id=None):
        if id:
            menu = db.session.get(Menu, id)
            if not menu:
                return abort(404, message='Menu not found')
            return jsonify(menu.to_json())
        else:
            menus = Menu.query.all()
            return jsonify([menu.to_json() for menu in menus])

    def post(self, restaurant_id):
        args = menu_parser.parse_args()
        new_menu_item = Menu(
            restaurant_id=restaurant_id,
            menu_name=args['menu_name'],
            price=args['price']
        )
        db.session.add(new_menu_item)
        db.session.commit()
        return {'message': 'Menu item created'}, 201

    def put(self, menu_id):
        menu = db.session.get(Menu, menu_id)
        if not menu:
            abort(404, message='Menu not found')

        args = menu_parser.parse_args()
        menu.menu_name = args['menu_name']
        menu.price = args['price']
        db.session.commit()
        return {'message': 'Menu updated'}

    def delete(self, menu_id):
        menu = db.session.get(Menu, menu_id)
        if not menu:
            abort(404, message='Menu not found')

        db.session.delete(menu)
        db.session.commit()
        return {'message': 'Menu deleted'}


# Add Resources to API
api.add_resource(UserResource, '/users', '/users/<int:user_id>')
api.add_resource(RestaurantResource, '/restaurants', '/restaurants/<int:restaurant_id>')
api.add_resource(MenuResource, '/restaurants/<int:restaurant_id>/menu')

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
