from flask_restful import Resource, reqparse, abort
from ..models import db, Dish_Additives


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
        return {'message': 'Additive created'}, 201

    def put(self, additive_id):
        additive = db.session.get(Dish_Additives, additive_id)
        if not additive:
            abort(404, message='Additive not found')

        args = additive_parser.parse_args()
        additive.additive_name = args['additive_name']
        additive.price = args['price']
        db.session.commit()
        return {'message': 'Additive updated'}, 200

    def delete(self, additive_id):
        additive = db.session.get(Dish_Additives, additive_id)
        if not additive:
            abort(404, message='Additive not found')

        db.session.delete(additive)
        db.session.commit()
        return {'message': 'Additive deleted'}, 200
