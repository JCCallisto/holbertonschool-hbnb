from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import facade

api = Namespace('places', description='Place operations')

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
        """Create a new place"""
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
        """Get all places"""
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
        """Get place details by ID"""
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
        """Update place by ID"""
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
