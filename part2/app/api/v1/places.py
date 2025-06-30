from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import HBnBFacade

api = Namespace('places', description='Place operations')

facade = HBnBFacade()

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude coordinate'),
    'longitude': fields.Float(required=True, description='Longitude coordinate'),
    'owner_id': fields.String(required=True, description='ID of the place owner'),
    'amenity_ids': fields.List(fields.String, description='List of amenity IDs')
})

place_response_model = api.model('PlaceResponse', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude coordinate'),
    'longitude': fields.Float(description='Longitude coordinate'),
    'owner_id': fields.String(description='ID of the place owner'),
    'amenity_ids': fields.List(fields.String, description='List of amenity IDs'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})

owner_model = api.model('Owner', {
    'id': fields.String(description='Owner ID'),
    'first_name': fields.String(description='Owner first name'),
    'last_name': fields.String(description='Owner last name'),
    'email': fields.String(description='Owner email')
})

amenity_model_simple = api.model('AmenitySimple', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Amenity name')
})

place_detailed_response_model = api.model('PlaceDetailedResponse', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude coordinate'),
    'longitude': fields.Float(description='Longitude coordinate'),
    'owner': fields.Nested(owner_model, description='Owner details'),
    'amenities': fields.List(fields.Nested(amenity_model_simple), description='List of amenities'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})

place_update_model = api.model('PlaceUpdate', {
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude coordinate'),
    'longitude': fields.Float(description='Longitude coordinate'),
    'amenity_ids': fields.List(fields.String, description='List of amenity IDs')
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created', place_response_model)
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Owner or amenity not found')
    def post(self):
        try:
            place_data = api.payload
            place = facade.create_place(place_data)
            return place.to_dict(), 201
        except ValueError as e:
            if "not found" in str(e):
                api.abort(404, str(e))
            else:
                api.abort(400, str(e))
        except Exception as e:
            api.abort(400, f"Invalid input data: {str(e)}")

    @api.response(200, 'List of places retrieved successfully', [place_detailed_response_model])
    def get(self):
        try:
            places = facade.get_all_places_with_details()
            return [place.to_dict(include_owner=True, include_amenities=True) for place in places], 200
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")


@api.route('/<string:place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully', place_detailed_response_model)
    @api.response(404, 'Place not found')
    def get(self, place_id):
        try:
            place = facade.get_place_with_details(place_id)
            if not place:
                api.abort(404, 'Place not found')
            return place.to_dict(include_owner=True, include_amenities=True), 200
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")

    @api.expect(place_update_model, validate=True)
    @api.response(200, 'Place updated successfully', place_response_model)
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Place, owner or amenity not found')
    def put(self, place_id):
        try:
            place_data = api.payload
            
            existing_place = facade.get_place(place_id)
            if not existing_place:
                api.abort(404, 'Place not found')
            
            updated_place = facade.update_place(place_id, place_data)
            if not updated_place:
                api.abort(404, 'Place not found')
            
            return updated_place.to_dict(), 200
        except ValueError as e:
            if "not found" in str(e):
                api.abort(404, str(e))
            else:
                api.abort(400, str(e))
        except Exception as e:
            api.abort(400, f"Invalid input data: {str(e)}")
from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import HBnBFacade

api = Namespace('amenities', description='Amenity operations')

facade = HBnBFacade()

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

amenity_response_model = api.model('AmenityResponse', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})

amenity_update_model = api.model('AmenityUpdate', {
    'name': fields.String(description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created', amenity_response_model)
    @api.response(400, 'Invalid input data')
    @api.response(409, 'Amenity name already exists')
    def post(self):
        try:
            amenity_data = api.payload
            amenity = facade.create_amenity(amenity_data)
            return amenity.to_dict(), 201
        except ValueError as e:
            if "Amenity name already exists" in str(e):
                api.abort(409, str(e))
            else:
                api.abort(400, str(e))
        except Exception as e:
            api.abort(400, f"Invalid input data: {str(e)}")

    @api.response(200, 'List of amenities retrieved successfully', [amenity_response_model])
    def get(self):
        try:
            amenities = facade.get_all_amenities()
            return [amenity.to_dict() for amenity in amenities], 200
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")


@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully', amenity_response_model)
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        try:
            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                api.abort(404, 'Amenity not found')
            return amenity.to_dict(), 200
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")

    @api.expect(amenity_update_model, validate=True)
    @api.response(200, 'Amenity updated successfully', amenity_response_model)
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Amenity not found')
    @api.response(409, 'Amenity name already exists')
    def put(self, amenity_id):
        try:
            amenity_data = api.payload
            
            existing_amenity = facade.get_amenity(amenity_id)
            if not existing_amenity:
                api.abort(404, 'Amenity not found')
            
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            if not updated_amenity:
                api.abort(404, 'Amenity not found')
            
            return updated_amenity.to_dict(), 200
        except ValueError as e:
            if "Amenity name already exists" in str(e):
                api.abort(409, str(e))
            else:
                api.abort(400, str(e))
        except Exception as e:
            api.abort(400, f"Invalid input data: {str(e)}")
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
