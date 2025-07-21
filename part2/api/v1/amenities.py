from flask_restx import Namespace, Resource, fields, reqparse
from business.facade import HBnBFacade

api = Namespace("amenities", description="Amenity related operations")
facade = HBnBFacade()

amenity_model = api.model("Amenity", {
    "id": fields.String(readonly=True, description="Amenity unique identifier"),
    "name": fields.String(required=True, description="Amenity name"),
})

amenity_create_parser = reqparse.RequestParser()
amenity_create_parser.add_argument("name", required=True)

amenity_update_parser = reqparse.RequestParser()
amenity_update_parser.add_argument("name")

@api.route("/")
class AmenityList(Resource):
    @api.marshal_list_with(amenity_model)
    def get(self):
        """List all amenities"""
        amenities = facade.list_amenities()
        return [a.to_dict() for a in amenities]

    @api.expect(amenity_create_parser)
    @api.marshal_with(amenity_model, code=201)
    def post(self):
        """Create a new amenity"""
        args = amenity_create_parser.parse_args()
        amenity = facade.create_amenity(args)
        return amenity.to_dict(), 201

@api.route("/<string:amenity_id>")
@api.response(404, "Amenity not found")
class Amenity(Resource):
    @api.marshal_with(amenity_model)
    def get(self, amenity_id):
        """Fetch an amenity by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")
        return amenity.to_dict()

    @api.expect(amenity_update_parser)
    @api.marshal_with(amenity_model)
    def put(self, amenity_id):
        """Update an amenity"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")
        args = {k: v for k, v in amenity_update_parser.parse_args().items() if v is not None}
        updated = facade.update_amenity(amenity_id, args)
        return updated.to_dict()
