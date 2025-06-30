from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('places', description='Place operations')
facade = HBnBFacade()

place_model = api.model('Place', {
    'title': fields.String(required=True),
    'description': fields.String,
    'price': fields.Float(required=True),
    'latitude': fields.Float(required=True),
    'longitude': fields.Float(required=True),
    'owner_id': fields.String(required=True),
    'amenity_ids': fields.List(fields.String)
})
place_response = api.model('PlaceResponse', {
    'id': fields.String,
    'title': fields.String,
    'description': fields.String,
    'price': fields.Float,
    'latitude': fields.Float,
    'longitude': fields.Float,
    'owner_id': fields.String,
    'amenity_ids': fields.List(fields.String),
    'created_at': fields.String,
    'updated_at': fields.String
})
place_detailed = api.model('PlaceDetailed', {
    'id': fields.String,
    'title': fields.String,
    'description': fields.String,
    'price': fields.Float,
    'latitude': fields.Float,
    'longitude': fields.Float,
    'owner': fields.Raw,  # Nested user
    'amenities': fields.List(fields.Raw), # List of nested amenities
    'reviews': fields.List(fields.Raw),   # List of nested reviews
    'created_at': fields.String,
    'updated_at': fields.String
})
place_update = api.model('PlaceUpdate', {
    'title': fields.String,
    'description': fields.String,
    'price': fields.Float,
    'latitude': fields.Float,
    'longitude': fields.Float,
    'amenity_ids': fields.List(fields.String)
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Created', place_response)
    @api.response(400, 'Invalid input')
    @api.response(404, 'Owner or Amenity not found')
    def post(self):
        try:
            place = facade.create_place(api.payload)
            return place.to_dict(), 201
        except ValueError as e:
            if "not found" in str(e).lower():
                api.abort(404, str(e))
            api.abort(400, str(e))

    @api.response(200, 'Success', [place_detailed])
    def get(self):
        return [
            p[0].to_dict(owner=p[1], amenities=p[2], reviews=p[3])
            for p in facade.get_all_places_with_details()
        ], 200

@api.route('/<string:place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Success', place_detailed)
    @api.response(404, 'Not found')
    def get(self, place_id):
        data = facade.get_place_with_details(place_id)
        if not data:
            api.abort(404, "Place not found")
        place, owner, amenities, reviews = data
        return place.to_dict(owner=owner, amenities=amenities, reviews=reviews), 200

    @api.expect(place_update, validate=True)
    @api.response(200, 'Updated', place_response)
    @api.response(400, 'Invalid input')
    @api.response(404, 'Not found')
    def put(self, place_id):
        try:
            place = facade.update_place(place_id, api.payload)
            if not place:
                api.abort(404, "Place not found")
            return place.to_dict(), 200
        except ValueError as e:
            if "not found" in str(e).lower():
                api.abort(404, str(e))
            api.abort(400, str(e))
