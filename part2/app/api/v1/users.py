from flask_restx import Namespace, Resource, fields
from ...services.facade import HBnBFacade

api = Namespace('users', description='User operations')
facade = HBnBFacade()

user_model = api.model('User', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'is_admin': fields.Boolean(default=False)
})
user_response = api.model('UserResponse', {
    'id': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'is_admin': fields.Boolean,
    'created_at': fields.String,
    'updated_at': fields.String
})
user_update = api.model('UserUpdate', {
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'password': fields.String
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'Created', user_response)
    @api.response(400, 'Invalid input')
    @api.response(409, 'Email exists')
    def post(self):
        try:
            user = facade.create_user(api.payload)
            return user.to_dict(), 201
        except ValueError as e:
            if "exists" in str(e):
                api.abort(409, str(e))
            api.abort(400, str(e))

    @api.response(200, 'Success', [user_response])
    def get(self):
        return [u.to_dict() for u in facade.get_all_users()], 200

@api.route('/<string:user_id>')
class UserResource(Resource):
    @api.response(200, 'Success', user_response)
    @api.response(404, 'Not found')
    def get(self, user_id):
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, "User not found")
        return user.to_dict(), 200

    @api.expect(user_update, validate=True)
    @api.response(200, 'Updated', user_response)
    @api.response(400, 'Invalid input')
    @api.response(404, 'Not found')
    @api.response(409, 'Email exists')
    def put(self, user_id):
        try:
            user = facade.update_user(user_id, api.payload)
            if not user:
                api.abort(404, "User not found")
            return user.to_dict(), 200
        except ValueError as e:
            if "exists" in str(e):
                api.abort(409, str(e))
            api.abort(400, str(e))
