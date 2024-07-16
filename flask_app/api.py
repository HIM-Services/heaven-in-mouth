from flask import Flask
from flask_restful import Api
from config import Config
from models import db


# Import resources
from resources.user import UserResource
from resources.restaurant import RestaurantResource
from resources.menu import MenuResource


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
api = Api(app)

# Register resources
api.add_resource(UserResource, '/users', '/users/<int:user_id>')
api.add_resource(RestaurantResource, '/restaurants', '/restaurants/<int:restaurant_id>')
api.add_resource(MenuResource, '/restaurants/<int:restaurant_id>/menu')


if __name__ == '__main__':
    app.run(debug=True)
