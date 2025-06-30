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
        """Create a new amenity"""
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
        """Get all amenities"""
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
        """Get amenity details by ID"""
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
        """Update amenity by ID"""
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
