from flask import session
from flask_restful import Resource


class LogoutResource(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            # Clear session data
            session.clear()
            return {'message': 'Logged out successfully'}, 200
        else:
            return {'message': 'User is not logged in'}, 401
