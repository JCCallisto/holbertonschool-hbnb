from flask_restx import Namespace, Resource, fields, reqparse
from business.facade import HBnBFacade

api = Namespace("users", description="User related operations")
facade = HBnBFacade()

user_model = api.model("User", {
    "id": fields.String(readonly=True, description="User unique identifier"),
    "email": fields.String(required=True, description="User email"),
    "first_name": fields.String(required=True, description="First name"),
    "last_name": fields.String(required=True, description="Last name"),
})

user_create_parser = reqparse.RequestParser()
user_create_parser.add_argument("email", required=True, help="Email cannot be blank")
user_create_parser.add_argument("first_name", required=True)
user_create_parser.add_argument("last_name", required=True)
user_create_parser.add_argument("password", required=True)

user_update_parser = reqparse.RequestParser()
user_update_parser.add_argument("email")
user_update_parser.add_argument("first_name")
user_update_parser.add_argument("last_name")

@api.route("/")
class UserList(Resource):
    @api.marshal_list_with(user_model)
    def get(self):
        """List all users"""
        users = facade.list_users()
        return [u.to_dict() for u in users]

    @api.expect(user_create_parser)
    @api.marshal_with(user_model, code=201)
    def post(self):
        """Create a new user"""
        args = user_create_parser.parse_args()
        user = facade.create_user(args)
        return user.to_dict(), 201

@api.route("/<string:user_id>")
@api.response(404, "User not found")
class User(Resource):
    @api.marshal_with(user_model)
    def get(self, user_id):
        """Fetch a user given its identifier"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, "User not found")
        return user.to_dict()

    @api.expect(user_update_parser)
    @api.marshal_with(user_model)
    def put(self, user_id):
        """Update a user given its identifier"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, "User not found")
        args = {k: v for k, v in user_update_parser.parse_args().items() if v is not None}
        updated = facade.update_user(user_id, args)
        return updated.to_dict()
