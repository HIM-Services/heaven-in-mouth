from flask import Flask
from flask_cors import CORS
from flask_session import Session
from flask_restful import Api
from config import Config
from models import db


# Import resources
from resources.user import UserResource, UserAliasResource
from resources.restaurant import RestaurantResource, RestaurantAliasResource
from resources.menu import MenuResource
from resources.login import LoginResource
from resources.logout import LogoutResource
from resources.dish import DishResource
from resources.dish_additives import DishAdditivesResource
from resources.address import AddressResource
from resources.nearby_restaurants import NearbyRestaurantsResource


app = Flask(__name__)
app.config.from_object(Config)
# TODO: For now we let all servers to reach out to flask server and post via CORS
# later on we should specify explicitly which servers we want to grant access to
# Look at this documentation page https://pypi.org/project/Flask-Cors/ under "Resource Specific CORS" section
CORS(app)

Session(app)  # Initialize session

db.init_app(app)
api = Api(app)

# Register resources
api.add_resource(UserResource, '/users', '/users/<int:user_id>')
api.add_resource(UserAliasResource, '/users', '/users/<string:user_name>')
api.add_resource(NearbyRestaurantsResource, '/users/<int:user_id>/nearby')
api.add_resource(RestaurantResource,
                 '/restaurants',
                 '/restaurants/<string:restaurant_name>/<int:restaurant_id>',
                 '/restaurants/<string:restaurant_name>')

api.add_resource(RestaurantAliasResource, '/restaurants', '/restaurants/<string:restaurant_name>/<int:restaurant_id>', '/restaurants/<string:restaurant_name>')
api.add_resource(MenuResource, '/restaurants/<int:restaurant_id>/menu', '/menu/<int:menu_id>')
api.add_resource(DishResource, '/menu/<int:menu_id>/dishes', '/dishes/<int:dish_id>')
api.add_resource(DishAdditivesResource, '/dishes/<int:dish_id>/additives', '/additives/<int:additive_id>')
api.add_resource(AddressResource, '/users/<int:user_id>/address', '/address/<int:address_id>')
api.add_resource(LoginResource, '/login')
api.add_resource(LogoutResource, '/logout')


# Endpoint for flask checks
@app.route('/flask', methods=['GET'])
def flask_check():
    return {"message": "Flask is running and accepting requests"}, 200


if __name__ == '__main__':
    app.run(debug=True)
