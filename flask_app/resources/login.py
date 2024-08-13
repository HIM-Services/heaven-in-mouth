from flask import session
from flask_restful import Resource, reqparse, abort
from werkzeug.security import check_password_hash
from models import Users
import logging
from resources.settings import set_logger

# Configure logging
set_logger()

# Parsers that check if the request has the required fields
user_parser = reqparse.RequestParser()
user_parser.add_argument('email', type=str, required=True, help="Email cannot be blank!")
user_parser.add_argument('password', type=str, required=True, help="Password cannot be blank!")


class LoginResource(Resource):
    # Check if a user is logged in
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            logging.warning('User is logged in')
            return {'message': 'User is logged in', 'user_id': user_id}, 200
        else:
            logging.error('User is not logged in')
            return {'message': 'User is not logged in'}, 401

    # Login a user
    def post(self):
        user_id = session.get('user_id')
        if user_id:
            abort(400, message='User is already logged in')
            logging.error('User is already logged in')
        args = user_parser.parse_args()
        user = Users.query.filter_by(email=args['email']).first()

        if not user:
            abort(404, message='User not found')
            logging.error('User not found')

        if not check_password_hash(user.password, args['password']):
            abort(401, message='Incorrect password')
            logging.error('Incorrect password')

        session['user_id'] = user.user_id
        session['csrf_token'] = 'some_csrf_token'  # Generate CSRF token as needed
        session['admin'] = user.admin
        session['email'] = user.email
        logging.warning('Logged in successfully')
        return {'message': 'Logged in successfully'}, 200
