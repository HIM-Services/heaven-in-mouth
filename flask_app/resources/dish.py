from flask_restful import Resource, reqparse, abort
from models import db, Dishes
import logging


# Parsers that check if the request has the required fields
dish_parser = reqparse.RequestParser()
dish_parser.add_argument('dish_name', type=str, required=True, help="Dish name cannot be blank!")
dish_parser.add_argument('price', type=float, required=True, help="Price cannot be blank!")
dish_parser.add_argument('ingredients', type=str, required=True, help="Description cannot be blank!")


class DishResource(Resource):
    def get(self, dish_id=None):
        # Get a specific dish by ID
        dish = db.session.get(Dishes, dish_id)
        if not dish:
            abort(404, message='Dish not found')
            logging.error('Dish not found')
        logging.warning('Dish found')
        return dish.to_json(), 200

    def post(self, menu_id):
        args = dish_parser.parse_args()
        new_dish = Dishes(
            menu_id=menu_id,
            dish_name=args['dish_name'],
            price=args['price'],
            ingredients=args['ingredients'],
        )
        db.session.add(new_dish)
        db.session.commit()
        logging.warning('Dish created')
        return {'message': 'Dish created'}, 201

    def put(self, dish_id):
        dish = db.session.get(Dishes, dish_id)
        if not dish:
            abort(404, message='Dish not found')
            logging.error('Dish not found')
        args = dish_parser.parse_args()
        dish.dish_name = args['dish_name']
        dish.price = args['price']
        dish.ingredients = args['ingredients']
        db.session.commit()
        logging.warning('Dish updated')
        return {'message': 'Dish updated'}, 200

    def delete(self, dish_id):
        dish = db.session.get(Dishes, dish_id)
        if not dish:
            abort(404, message='Dish not found')
            logging.error('Dish not found')

        db.session.delete(dish)
        db.session.commit()
        logging.warning('Dish deleted')
        return {'message': 'Dish deleted'}, 200
