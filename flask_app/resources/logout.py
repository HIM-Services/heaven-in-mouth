from flask import session
from flask_restful import Resource
import logging

# logging configuration

logging.basicConfig(filename='main.log', level=logging.DEBUG, format=('%(asctime)s %(levelname)s : %(message)s'))


class LogoutResource(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            # Clear session data
            session.clear()
            logging.info('Logged out successfully')
            return {'message': 'Logged out successfully'}, 200
        else:
            logging.error('User is not logged in')
            return {'message': 'User is not logged in'}, 401
