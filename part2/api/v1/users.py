from flask_restx import Namespace, Resource, fields, reqparse
from business.facade import hbnb_facade

api = Namespace('users', description="User operations")

user_model = api.model('User', {
    'id': fields.String(readonly=True),
    'email': fields.String(required=True),
    'first_name': fields.String,
    'last_name': fields.String,
    'created_at': fields.String,
    'updated_at': fields.String,
  
})

user_create = api.model('UserCreate', {
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'first_name': fields.String,
    'last_name': fields.String,
})

user_update = api.model('UserUpdate', {
    'first_name': fields.String,
    'last_name': fields.String,
    'password': fields.String,
})

@api.route('/')
class UserList(Resource):
    @api.marshal_list_with(user_model)
    def get(self):
        """List all users (password omitted)"""
        return hbnb_facade.list_users()

    @api.expect(user_create)
    @api.marshal_with(user_model, code=201)
    def post(self):
        """Create a new user"""
        data = api.payload
        return hbnb_facade.create_user(data), 201

@api.route('/<string:user_id>')
class UserResource(Resource):
    @api.marshal_with(user_model)
    def get(self, user_id):
        """Get user by ID (password omitted)"""
        return hbnb_facade.get_user(user_id)

@api.expect(user_update)
@api.marshal_with(user_model)
def put(self, user_id):
    """Update user details"""
    data = api.payload
    return hbnb_facade.update_user(user_id, data)

def delete(self, user_id):
    """Delete a user by ID"""
    result = hbnb_facade.delete_user(user_id)
    if result:
        return '', 204
    else:
        return {"message": "User not found"}, 404

@api.route('/<string:user_id>')
class UserResource(Resource):
    def get(self, user_id):
        user = hbnb_facade.get_user(user_id)
        if user:
            return user, 200
        else:
            return {"message": "User not found"}, 404
