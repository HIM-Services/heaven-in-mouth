from flask_restful import Resource, reqparse, abort
from werkzeug.security import generate_password_hash
from models import db, Users


# Parsers that check if the request has the required fields
user_parser = reqparse.RequestParser()
user_parser.add_argument('name', type=str, required=True, help='Name is required')
user_parser.add_argument('user_name', type=str, required=True, help='Username is required')
user_parser.add_argument('email', type=str, required=True, help='Email is required')
user_parser.add_argument('phone', type=str, required=True, help='Phone is required')
user_parser.add_argument('password', type=str, required=True, help='Password is required')


class UserResource(Resource):
    # Get all users or a specific user
    def get(self, user_name=None):
        if user_name:
            user = Users.query.filter_by(user_name=user_name).first()
            if not user:
                abort(404, message='User not found')
            return user.to_json(), 200
        else:
            users = Users.query.all()
            return [user.to_json() for user in users], 200

    # Create a new user
    def post(self):
        args = user_parser.parse_args()

        # Check if a user with the same email already exists
        existing_user = Users.query.filter_by(email=args['email']).first()
        if existing_user:
            return {'message': 'User with the same email already exists'}, 400
        # check if a user with the same username already exists
        if Users.query.filter_by(user_name=args['user_name']).first():
            return {'message': 'User with the same username already exists'}, 400

        new_user = Users(
            name=args['name'],
            user_name=args['user_name'],
            email=args['email'],
            phone=args['phone'],
            password=generate_password_hash(args['password'])
        )

        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User created'}, 201

    # Update a user
    def put(self, user_name):
        user = db.session.get(Users, user_name)
        if not user:
            abort(404, message='User not found')

        args = user_parser.parse_args()
        user.name = args['name']
        user.user_name = args['user_name']
        user.email = args['email']
        user.phone = args['phone']
        user.password = generate_password_hash(args['password'])
        db.session.commit()
        return {'message': 'User updated'}, 200

    # Delete a user
    def delete(self, user_name):
        user = db.session.get(Users, user_name)
        if not user:
            abort(404, message='User not found')

        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted'}, 200
