from flask_restful import Resource, reqparse, abort
from models import db, Menu
import logging

# logging configuration
logging.basicConfig(filename='main.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s : %(message)s')

# Parsers that check if the request has the required fields
menu_parser = reqparse.RequestParser()
menu_parser.add_argument('menu_name', type=str, required=True, help="Menu name cannot be blank!")


class MenuResource(Resource):
    def get(self, menu_id):
        menu = db.session.get(Menu, menu_id)
        if not menu:
            logging.error('Menu not found')
            return abort(404, message='Menu not found')
        logging.info('Menu found')
        return menu.to_json(), 200

    def post(self, restaurant_id):
        args = menu_parser.parse_args()
        new_menu = Menu(
            restaurant_id=restaurant_id,
            menu_name=args['menu_name'],
        )
        db.session.add(new_menu)
        db.session.commit()
        logging.info('Menu created')
        return {'message': 'Menu created'}, 201

    def put(self, menu_id):
        menu = db.session.get(Menu, menu_id)
        if not menu:
            logging.error('Menu not found')
            abort(404, message='Menu not found')

        args = menu_parser.parse_args()
        menu.menu_name = args['menu_name']
        db.session.commit()
        logging.info('Menu updated')
        return {'message': 'Menu updated'}, 200

    def delete(self, menu_id):
        menu = db.session.get(Menu, menu_id)
        if not menu:
            logging.error('Menu not found')
            abort(404, message='Menu not found')

        db.session.delete(menu)
        db.session.commit()
        logging.info('Menu deleted')
        return {'message': 'Menu deleted'}, 200
