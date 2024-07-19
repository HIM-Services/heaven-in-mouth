from flask_restful import Resource, reqparse, abort
from models import db, Menu


# Parsers that check if the request has the required fields
menu_parser = reqparse.RequestParser()
menu_parser.add_argument('menu_name', type=str, required=True, help="Menu name cannot be blank!")


class MenuResource(Resource):
    def get(self, menu_id):
        menu = db.session.get(Menu, menu_id)
        if not menu:
            return abort(404, message='Menu not found')

        return menu.to_json(), 200

    def post(self, restaurant_id):
        args = menu_parser.parse_args()
        new_menu = Menu(
            restaurant_id=restaurant_id,
            menu_name=args['menu_name'],
        )
        db.session.add(new_menu)
        db.session.commit()
        return {'message': 'Menu created'}, 201

    def put(self, menu_id):
        menu = db.session.get(Menu, menu_id)
        if not menu:
            abort(404, message='Menu not found')

        args = menu_parser.parse_args()
        menu.menu_name = args['menu_name']
        db.session.commit()
        return {'message': 'Menu updated'}, 200

    def delete(self, menu_id):
        menu = db.session.get(Menu, menu_id)
        if not menu:
            abort(404, message='Menu not found')

        db.session.delete(menu)
        db.session.commit()
        return {'message': 'Menu deleted'}, 200
