from flask_restful import Resource, reqparse, abort
from werkzeug.security import generate_password_hash
from models import db, Users
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s : %(message)s',
    handlers=[
        logging.FileHandler('main.log'),
        logging.StreamHandler()
    ]
)

# Disable Flask's default logging for requests
logging.getLogger('werkzeug').setLevel(logging.WARNING)
logging.getLogger('sqlalchemy').setLevel(logging.WARNING)
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

# Parsers that check if the request has the required fields
user_parser = reqparse.RequestParser()
user_parser.add_argument('name', type=str, required=True,
                         help="Name cannot be blank!")
user_parser.add_argument('email', type=str, required=True,
                         help="Email cannot be blank!")
user_parser.add_argument('phone', type=str, required=True,
                         help="Phone cannot be blank!")
user_parser.add_argument('password', type=str,
                         required=True, help="Password cannot be blank!")


class UserResource(Resource):
    # Get all users or a specific user
    def get(self, user_id=None):
        if user_id:
            user = db.session.get(Users, user_id)
            if not user:
                logging.warning('User not found')
                abort(404, message='User not found')
            logging.warning('User found')
            return user.to_json(), 200
        else:
            users = Users.query.all()
            logging.warning('Users found')
            return [user.to_json() for user in users], 200

    # Create a new user
    def post(self):
        args = user_parser.parse_args()

        # Check if a user with the same email already exists
        existing_user = Users.query.filter_by(email=args['email']).first()
        if existing_user:
            logging.warning('User with the same email already exists')
            abort(400, message='User with the same email already exists')

        new_user = Users(
            name=args['name'],
            email=args['email'],
            phone=args['phone'],
            password=generate_password_hash(args['password'])
        )

        db.session.add(new_user)
        db.session.commit()
        logging.warning('User created')
        return {'message': 'User created'}, 201

    # Update a user
    def put(self, user_id):
        user = db.session.get(Users, user_id)
        if not user:
            logging.warning('User not found')
            abort(404, message='User not found')

        args = user_parser.parse_args()
        user.name = args['name']
        user.email = args['email']
        user.phone = args['phone']
        user.password = generate_password_hash(args['password'])
        db.session.commit()
        logging.warning('User updated')
        return {'message': 'User updated'}, 200

    # Delete a user
    def delete(self, user_id):
        user = db.session.get(Users, user_id)
        if not user:
            logging.warning('User not found')
            abort(404, message='User not found')

        db.session.delete(user)
        db.session.commit()
        logging.warning('User deleted')
        return {'message': 'User deleted'}, 200
