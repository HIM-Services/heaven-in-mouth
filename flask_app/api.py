from flask import Flask
from flask_session import Session
from flask_restful import Api
from config import Config
from models import db
from sqlalchemy.sql import text


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

Session(app)  # Initialize session

db.init_app(app)
api = Api(app)

# Register resources
api.add_resource(UserResource, '/users', '/users/<int:user_id>')
api.add_resource(UserAliasResource, '/users', '/users/<string:user_name>')
api.add_resource(NearbyRestaurantsResource, '/users/<int:user_id>/nearby')
api.add_resource(RestaurantResource, '/restaurants', '/restaurants/<int:restaurant_id>')
api.add_resource(RestaurantAliasResource, '/restaurants', '/restaurants/<string:restaurant_name>')
api.add_resource(MenuResource, '/restaurants/<int:restaurant_id>/menu', '/menu/<int:menu_id>')
api.add_resource(DishResource, '/menu/<int:menu_id>/dishes', '/dishes/<int:dish_id>')
api.add_resource(DishAdditivesResource, '/dishes/<int:dish_id>/additives', '/additives/<int:additive_id>')
api.add_resource(AddressResource, '/users/<int:user_id>/address', '/address/<int:address_id>')
api.add_resource(LoginResource, '/login')
api.add_resource(LogoutResource, '/logout')


# Endpoint for flasm checks
@app.route('/flask', methods=['GET'])
def flask_check():
    return {"message": "Flask is running"}, 200


# Endpoint to check if Flask can connect to Postgres
@app.route('/check_db', methods=['GET'])
def check_db():
    try:
        # Simple query to check if Flask can connect to Postgres
        db.session.execute(text('SELECT 1'))
        return {"message": "Flask can connect to Postgres"}, 200
    except Exception as e:
        return {"message": f"Flask cannot connect to Postgres: {str(e)}"}, 500


if __name__ == '__main__':
    app.run(debug=True)
