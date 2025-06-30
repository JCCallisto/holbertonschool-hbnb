from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import HBnBFacade

api = Namespace('users', description='User operations')

facade = HBnBFacade()

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
    'is_admin': fields.Boolean(description='Admin status of the user', default=False)
})

user_response_model = api.model('UserResponse', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user'),
    'is_admin': fields.Boolean(description='Admin status of the user'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})

user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user'),
    'password': fields.String(description='Password of the user')
})


@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created', user_response_model)
    @api.response(400, 'Invalid input data')
    @api.response(409, 'Email already exists')
    def post(self):
        try:
            user_data = api.payload
            user = facade.create_user(user_data)
            return user.to_dict(), 201
        except ValueError as e:
            if "Email already exists" in str(e):
                api.abort(409, str(e))
            else:
                api.abort(400, str(e))
        except Exception as e:
            api.abort(400, f"Invalid input data: {str(e)}")

    @api.response(200, 'List of users retrieved successfully', [user_response_model])
    def get(self):
        try:
            users = facade.get_all_users()
            return [user.to_dict() for user in users], 200
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")


@api.route('/<string:user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully', user_response_model)
    @api.response(404, 'User not found')
    def get(self, user_id):
        try:
            user = facade.get_user(user_id)
            if not user:
                api.abort(404, 'User not found')
            return user.to_dict(), 200
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")

    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User updated successfully', user_response_model)
    @api.response(400, 'Invalid input data')
    @api.response(404, 'User not found')
    @api.response(409, 'Email already exists')
    def put(self, user_id):
        try:
            user_data = api.payload
            
            existing_user = facade.get_user(user_id)
            if not existing_user:
                api.abort(404, 'User not found')
            
            updated_user = facade.update_user(user_id, user_data)
            if not updated_user:
                api.abort(404, 'User not found')
            
            return updated_user.to_dict(), 200
        except ValueError as e:
            if "Email already exists" in str(e):
                api.abort(409, str(e))
            else:
                api.abort(400, str(e))
        except Exception as e:
            api.abort(400, f"Invalid input data: {str(e)}")
