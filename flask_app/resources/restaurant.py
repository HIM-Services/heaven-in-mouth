from flask import jsonify
from flask_restful import Resource, reqparse, abort
from models import db, Restaurants


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
