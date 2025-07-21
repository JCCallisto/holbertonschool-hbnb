from flask_restx import Namespace, Resource, fields, reqparse
from business.facade import HBnBFacade

api = Namespace("places", description="Place related operations")
facade = HBnBFacade()

place_model = api.model("Place", {
    "id": fields.String(readonly=True, description="Place unique identifier"),
    "name": fields.String(required=True, description="Place name"),
    "description": fields.String(description="Place description"),
    "price": fields.Float(required=True, description="Price per night"),
    "latitude": fields.Float(description="Latitude"),
    "longitude": fields.Float(description="Longitude"),
    "owner_id": fields.String(required=True, description="User ID of owner"),
    "amenity_ids": fields.List(fields.String, description="List of Amenity IDs"),
})

place_create_parser = reqparse.RequestParser()
place_create_parser.add_argument("name", required=True)
place_create_parser.add_argument("owner_id", required=True)
place_create_parser.add_argument("price", type=float, required=True)
place_create_parser.add_argument("description")
place_create_parser.add_argument("latitude", type=float)
place_create_parser.add_argument("longitude", type=float)
place_create_parser.add_argument("amenity_ids", type=str, action="split")

place_update_parser = reqparse.RequestParser()
place_update_parser.add_argument("name")
place_update_parser.add_argument("description")
place_update_parser.add_argument("price", type=float)
place_update_parser.add_argument("latitude", type=float)
place_update_parser.add_argument("longitude", type=float)
place_update_parser.add_argument("amenity_ids", type=str, action="split")

@api.route("/")
class PlaceList(Resource):
    @api.marshal_list_with(place_model)
    def get(self):
        """List all places"""
        places = facade.list_places()
        return [p.to_dict() for p in places]

    @api.expect(place_create_parser)
    @api.marshal_with(place_model, code=201)
    def post(self):
        """Create a new place"""
        args = place_create_parser.parse_args()
        if args["amenity_ids"] is None:
            args["amenity_ids"] = []
        place = facade.create_place(args)
        return place.to_dict(), 201

@api.route("/<string:place_id>")
@api.response(404, "Place not found")
class Place(Resource):
    @api.marshal_with(place_model)
    def get(self, place_id):
        """Fetch a place by ID"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")
        return place.to_dict()

    @api.expect(place_update_parser)
    @api.marshal_with(place_model)
    def put(self, place_id):
        """Update a place"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")
        args = {k: v for k, v in place_update_parser.parse_args().items() if v is not None}
        updated = facade.update_place(place_id, args)
        return updated.to_dict()
