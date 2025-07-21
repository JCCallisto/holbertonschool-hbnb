from flask_restx import Namespace, Resource, fields, reqparse
from business.facade import HBnBFacade

api = Namespace("reviews", description="Review related operations")
facade = HBnBFacade()

review_model = api.model("Review", {
    "id": fields.String(readonly=True, description="Review unique identifier"),
    "user_id": fields.String(required=True, description="Reviewer User ID"),
    "place_id": fields.String(required=True, description="Reviewed Place ID"),
    "text": fields.String(required=True, description="Review text"),
})

review_create_parser = reqparse.RequestParser()
review_create_parser.add_argument("user_id", required=True)
review_create_parser.add_argument("place_id", required=True)
review_create_parser.add_argument("text", required=True)

review_update_parser = reqparse.RequestParser()
review_update_parser.add_argument("text")

@api.route("/")
class ReviewList(Resource):
    @api.marshal_list_with(review_model)
    def get(self):
        """List all reviews"""
        reviews = facade.list_reviews()
        return [r.to_dict() for r in reviews]

    @api.expect(review_create_parser)
    @api.marshal_with(review_model, code=201)
    def post(self):
        """Create a new review"""
        args = review_create_parser.parse_args()
        review = facade.create_review(args)
        return review.to_dict(), 201

@api.route("/<string:review_id>")
@api.response(404, "Review not found")
class Review(Resource):
    @api.marshal_with(review_model)
    def get(self, review_id):
        """Fetch a review by ID"""
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, "Review not found")
        return review.to_dict()

    @api.expect(review_update_parser)
    @api.marshal_with(review_model)
    def put(self, review_id):
        """Update a review"""
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, "Review not found")
        args = {k: v for k, v in review_update_parser.parse_args().items() if v is not None}
        updated = facade.update_review(review_id, args)
        return updated.to_dict()

    def delete(self, review_id):
        """Delete a review"""
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, "Review not found")
        facade.delete_review(review_id)
        return {}, 204
