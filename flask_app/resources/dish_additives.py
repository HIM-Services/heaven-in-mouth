from flask_restful import Resource, reqparse, abort
from models import db, Dish_Additives
import logging

# logging configuration
logging.basicConfig(filename='main.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s : %(message)s')

# Parsers that check if the request has the required fields
additive_parser = reqparse.RequestParser()
additive_parser.add_argument('additive_name', type=str, required=True, help="Additive name cannot be blank!")
additive_parser.add_argument('price', type=float, required=True, help="Price cannot be blank!")


class DishAdditivesResource(Resource):
    def get(self, additive_id=None):
        # Get a specific dish by ID
        additive = db.session.get(Dish_Additives, additive_id)
        if not additive:
            abort(404, message='Additive not found')
            logging.error('Additive not found')
        return additive.to_json(), 200

    def post(self, dish_id):
        args = additive_parser.parse_args()
        new_additive = Dish_Additives(
            dish_id=dish_id,
            additive_name=args['additive_name'],
            price=args['price'],
        )
        db.session.add(new_additive)
        db.session.commit()
        logging.info('Additive created')
        return {'message': 'Additive created'}, 201
        

    def put(self, additive_id):
        additive = db.session.get(Dish_Additives, additive_id)
        if not additive:
            abort(404, message='Additive not found')
            logging.error('Additive not found')
        args = additive_parser.parse_args()
        additive.additive_name = args['additive_name']
        additive.price = args['price']
        db.session.commit()
        logging.info('Additive created')
        return {'message': 'Additive updated'}, 200

    def delete(self, additive_id):
        additive = db.session.get(Dish_Additives, additive_id)
        if not additive:
            abort(404, message='Additive not found')
            logging.info('Additive created')

        db.session.delete(additive)
        db.session.commit()
        logging.info('Additive deleted')
        return {'message': 'Additive deleted'}, 200
