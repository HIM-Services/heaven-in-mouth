from flask_restful import Resource, reqparse, abort
from models import db, Address
from helpers import geocode_address
import logging
from resources.settings import set_logger

# Configure logging
set_logger()

# Parsers that check if the request has the required fields
address_parser = reqparse.RequestParser()
address_parser.add_argument('state', type=str, required=True, help="State cannot be blank!")
address_parser.add_argument('city', type=str, required=True, help="City name cannot be blank!")
address_parser.add_argument('street', type=str, required=True, help="Street cannot be blank!")
address_parser.add_argument('pincode', type=str, required=True, help="Pincode cannot be blank!")


# Address to which the user's order will be delivered
class AddressResource(Resource):
    def get(self, address_id=None):
        address = db.session.get(Address, address_id)
        if not address:
            abort(404, message='Address_id not found')
            logging.error('Address_id not found')
        logging.warning('Address found')
        return address.to_json(), 200

    def post(self, user_id):
        args = address_parser.parse_args()
        address_str = f"{args['street']}, {args['city']}, {args['state']}, {args['pincode']}"

        # Geocode the address
        try:
            geo_data = geocode_address(address_str)
        except Exception as e:
            abort(400, message=str(e))
            logging.error(str(e))

        new_address = Address(
            user_id=user_id,
            state=args['state'],
            city=args['city'],
            street=args['street'],
            pincode=args['pincode'],
            longitude=geo_data['longitude'],
            latitude=geo_data['latitude']
        )
        new_address.set_geolocation()
        db.session.add(new_address)
        db.session.commit()
        logging.warning('Address created')
        return {'message': 'Address created'}, 201

    def put(self, address_id):
        address = db.session.get(Address, address_id)
        if not address:
            abort(404, message='Address not found')
            logging.error('Address not found')

        args = address_parser.parse_args()
        address.state = args['state']
        address.city = args['city']
        address.street = args['street']
        address.pincode = args['pincode']

        address_str = f"{args['street']}, {args['city']}, {args['state']}, {args['pincode']}"
        try:
            geo_data = geocode_address(address_str)
            address.longitude = geo_data['longitude']
            address.latitude = geo_data['latitude']
            address.set_geolocation()
        except Exception as e:
            abort(400, message=str(e))
            logging.error(str(e))

        db.session.commit()
        logging.warning('Address updated')
        return {'message': 'Address updated'}, 200

    def delete(self, address_id):
        address = db.session.get(Address, address_id)
        if not address:
            abort(404, message='Address not found')
            logging.error('Address not found')

        db.session.delete(address)
        db.session.commit()
        logging.warning('Address deleted')
        return {'message': 'Address deleted'}, 200
