from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('amenities', description='Amenity operations')
facade = HBnBFacade()

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True)
})
amenity_response = api.model('AmenityResponse', {
    'id': fields.String,
    'name': fields.String,
    'created_at': fields.String,
    'updated_at': fields.String
})
amenity_update = api.model('AmenityUpdate', {
    'name': fields.String
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Created', amenity_response)
    @api.response(400, 'Invalid input')
    @api.response(409, 'Name exists')
    def post(self):
        try:
            amenity = facade.create_amenity(api.payload)
            return amenity.to_dict(), 201
        except ValueError as e:
            if "exists" in str(e):
                api.abort(409, str(e))
            api.abort(400, str(e))

    @api.response(200, 'Success', [amenity_response])
    def get(self):
        return [a.to_dict() for a in facade.get_all_amenities()], 200

@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Success', amenity_response)
    @api.response(404, 'Not found')
    def get(self, amenity_id):
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")
        return amenity.to_dict(), 200

    @api.expect(amenity_update, validate=True)
    @api.response(200, 'Updated', amenity_response)
    @api.response(400, 'Invalid input')
    @api.response(404, 'Not found')
    @api.response(409, 'Name exists')
    def put(self, amenity_id):
        try:
            amenity = facade.update_amenity(amenity_id, api.payload)
            if not amenity:
                api.abort(404, "Amenity not found")
            return amenity.to_dict(), 200
        except ValueError as e:
            if "exists" in str(e):
                api.abort(409, str(e))
            api.abort(400, str(e))
