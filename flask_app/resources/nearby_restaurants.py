from flask_restful import Resource, abort
from models import db, Address, Restaurants
from sqlalchemy import func
import logging


class NearbyRestaurantsResource(Resource):
    def get(self, user_id):
        radius = 5000

        # Get the user's geolocation
        user_geolocation = db.session.query(Address.geolocation).filter_by(user_id=user_id).first()

        if user_geolocation is None:
            logging.error('User not found')
            abort(404, message='User not found')

        # Get all restaurants within the radius
        nearby_restaurants = db.session.query(Restaurants).filter(
            func.ST_Distance(Restaurants.geolocation, user_geolocation[0]) <= radius
        ).all()
        logging.warning('Restaurants found')
        return [restaurant.to_json() for restaurant in nearby_restaurants], 200
