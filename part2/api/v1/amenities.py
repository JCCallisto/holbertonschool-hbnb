from flask_restx import Namespace, Resource, fields

from business.facade import hbnb_facade

api = Namespace('amenities', description="Amenity operations")

amenity_model = api.model('Amenity', {
    'id': fields.String(readonly=True),
    'name': fields.String(required=True),
    'created_at': fields.String,
    'updated_at': fields.String,
})

amenity_create = api.model('AmenityCreate', {
    'name': fields.String(required=True),
})

amenity_update = api.model('AmenityUpdate', {
    'name': fields.String,
})

@api.route('/')
class AmenityList(Resource):
    @api.marshal_list_with(amenity_model)
    def get(self):
        return hbnb_facade.list_amenities()

    @api.expect(amenity_create)
    @api.marshal_with(amenity_model, code=201)
    def post(self):
        data = api.payload
        return hbnb_facade.create_amenity(data), 201

@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @api.marshal_with(amenity_model)
    def get(self, amenity_id):
        return hbnb_facade.get_amenity(amenity_id)

    @api.expect(amenity_update)
    @api.marshal_with(amenity_model)
    def put(self, amenity_id):
        data = api.payload
        return hbnb_facade.update_amenity(amenity_id, data)
