from flask import Flask
from flask_session import Session
from flask_restful import Api
from config import Config
from models import db


# Import resources
from resources.user import UserResource
from resources.restaurant import RestaurantResource
from resources.menu import MenuResource
from resources.login import LoginResource
from resources.logout import LogoutResource


app = Flask(__name__)
app.config.from_object(Config)

Session(app)  # Initialize session

db.init_app(app)
api = Api(app)

# Register resources
api.add_resource(UserResource, '/users', '/users/<int:user_id>')
api.add_resource(RestaurantResource, '/restaurants', '/restaurants/<int:restaurant_id>')
api.add_resource(MenuResource, '/restaurants/<int:restaurant_id>/menu')
api.add_resource(LoginResource, '/login')
api.add_resource(LogoutResource, '/logout')


if __name__ == '__main__':
    app.run(debug=True)
