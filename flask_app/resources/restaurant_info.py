from flask_restful import Resource, fields, marshal_with, abort
from models import Restaurants, Menu, Rating


menu_fields = {
    'menu_id': fields.Integer,
    'menu_name': fields.String,
    'dishes': fields.List(fields.Nested({
        'dish_id': fields.Integer,
        'dish_name': fields.String,
        'price': fields.Float,
        'ingredients': fields.String
    }))
}

rating_fields = {
    'rating_id': fields.Integer,
    'user_id': fields.Integer,
    'rating': fields.Integer
}

restaurant_fields = {
    'restaurant_id': fields.Integer,
    'name': fields.String,
    'address': fields.String,
    'phone': fields.String,
    'menus': fields.List(fields.Nested(menu_fields)),
    'ratings': fields.List(fields.Nested(rating_fields)),
}


class RestaurantDetails(Resource):
    @marshal_with(restaurant_fields)
    def get(self, rest_id=None):
        if rest_id:
            restaurant = Restaurants.query.filter_by(restaurant_id=rest_id).first_or_404()
            restaurant.menus = Menu.query.filter_by(restaurant_id=rest_id).all()
            restaurant.ratings = Rating.query.filter_by(restaurant_id=rest_id).all()
        if not rest_id:
            abort(404, message='Restaurant not found')
        return restaurant
