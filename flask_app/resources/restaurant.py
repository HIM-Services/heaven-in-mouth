from flask import redirect
from flask_restful import Resource, reqparse, abort, url_for
from models import db, Restaurants
from helpers import geocode_address,validate_phone
import logging
from resources.settings import set_logger


# Parsers that check if the request has the required fields
restaurant_parser = reqparse.RequestParser()
restaurant_parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")
restaurant_parser.add_argument('address', type=str, required=True, help="Address cannot be blank!")
restaurant_parser.add_argument('phone', type=str, required=True, help="Phone cannot be blank!")


class RestaurantResource(Resource):
    # Get all restaurants or a specific restaurant
    def get(self, restaurant_id=None):
        if restaurant_id:
            restaurant = db.session.get(Restaurants, restaurant_id)
            if not restaurant:
                logging.error('Restaurant not found')
                abort(404, message='Restaurant not found')
            logging.warning('Restaurant found')
            return restaurant.to_json(True), 200
        else:
            restaurants = Restaurants.query.all()
            logging.warning('Restaurants found')
            return [restaurant.to_json() for restaurant in restaurants], 200

    # Create a new restaurant
    def post(self):
        args = restaurant_parser.parse_args()
        address = args['address']

        # Validate phone number
        if not validate_phone(args['phone']):
            return {'message': 'Invalid phone number'}, 400

        try:
            geo_data = geocode_address(address)
        except Exception as e:
            logging.error(str(e))
            abort(400, message=str(e))

        new_restaurant = Restaurants(
            name=args['name'],
            address=address,
            phone=args['phone'],
            longitude=geo_data['longitude'],
            latitude=geo_data['latitude']
        )
        new_restaurant.set_geolocation()
        db.session.add(new_restaurant)
        db.session.commit()
        logging.warning('Restaurant created')
        return {'message': 'Restaurant created'}, 201

    # Update a restaurant
    def put(self, restaurant_id):
        restaurant = db.session.get(Restaurants, restaurant_id)
        if not restaurant:
            logging.error('Restaurant not found')
            abort(404, message='Restaurant not found')

        args = restaurant_parser.parse_args()
        restaurant.name = args['name']
        restaurant.phone = args['phone']
        restaurant.address = args['address']
        # Validate phone number
        if not validate_phone(args['phone']):
            return {'message': 'Invalid phone number'}, 400

        # Update the geocoding data
        try:
            geo_data = geocode_address(args['address'])
            restaurant.longitude = geo_data['longitude']
            restaurant.latitude = geo_data['latitude']
            restaurant.set_geolocation()
        except Exception as e:
            logging.error(str(e))
            abort(400, message=str(e))

        db.session.commit()
        logging.warning('Restaurant updated')
        return {'message': 'Restaurant updated'}, 200

    # Delete a restaurant
    def delete(self, restaurant_id):
        restaurant = db.session.get(Restaurants, restaurant_id)
        if not restaurant:
            logging.error('Restaurant not found')
            abort(404, message='Restaurant not found')

        db.session.delete(restaurant)
        db.session.commit()
        logging.warning('Restaurant deleted')
        return {'message': 'Restaurant deleted'}, 200


class RestaurantAliasResource(Resource):
    def get(self, restaurant_name):
        restaurant_name = restaurant_name.replace('_', ' ')
        restaurant = Restaurants.query.filter_by(name=restaurant_name).first()
        if restaurant:
            return redirect(url_for('restaurantresource', restaurant_id=restaurant.restaurant_id), code=302)
        else:
            return {'message': 'Restaurant not found'}, 404
