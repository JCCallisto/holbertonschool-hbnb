from flask_restx import Namespace, Resource, fields

from business.facade import hbnb_facade

api = Namespace('places', description="Place operations")

place_model = api.model('Place', {
    'id': fields.String(readonly=True),
    'name': fields.String(required=True),
    'description': fields.String,
    'price': fields.Float,
    'latitude': fields.Float,
    'longitude': fields.Float,
    'owner_id': fields.String,
    'created_at': fields.String,
    'updated_at': fields.String,
    # Extended attributes
    'owner_first_name': fields.String,
    'owner_last_name': fields.String,
    'amenities': fields.List(fields.Nested(api.model('Amenity', {
        'id': fields.String,
        'name': fields.String,
    }))),
    'reviews': fields.List(fields.Nested(api.model('Review', {
        'id': fields.String,
        'text': fields.String,
        'user_id': fields.String,
    }))),
})

place_create = api.model('PlaceCreate', {
    'name': fields.String(required=True),
    'description': fields.String,
    'price': fields.Float,
    'latitude': fields.Float,
    'longitude': fields.Float,
    'owner_id': fields.String(required=True),
    'amenity_ids': fields.List(fields.String),
})

place_update = api.model('PlaceUpdate', {
    'name': fields.String,
    'description': fields.String,
    'price': fields.Float,
    'latitude': fields.Float,
    'longitude': fields.Float,
    'amenity_ids': fields.List(fields.String),
})

@api.route('/')
class PlaceList(Resource):
    @api.marshal_list_with(place_model)
    def get(self):
        return hbnb_facade.list_places()

    @api.expect(place_create)
    @api.marshal_with(place_model, code=201)
    def post(self):
        data = api.payload
        return hbnb_facade.create_place(data), 201

@api.route('/<string:place_id>')
class PlaceResource(Resource):
    @api.marshal_with(place_model)
    def get(self, place_id):
        return hbnb_facade.get_place(place_id)

    @api.expect(place_update)
    @api.marshal_with(place_model)
    def put(self, place_id):
        data = api.payload
        return hbnb_facade.update_place(place_id, data)
