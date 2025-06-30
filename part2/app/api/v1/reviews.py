from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('reviews', description='Review operations')
facade = HBnBFacade()

review_model = api.model('Review', {
    'text': fields.String(required=True),
    'rating': fields.Integer(required=True),
    'place_id': fields.String(required=True),
    'user_id': fields.String(required=True)
})
review_response = api.model('ReviewResponse', {
    'id': fields.String,
    'text': fields.String,
    'rating': fields.Integer,
    'user_id': fields.String,
    'place_id': fields.String,
    'created_at': fields.String,
    'updated_at': fields.String
})
review_update = api.model('ReviewUpdate', {
    'text': fields.String,
    'rating': fields.Integer
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, 'Created', review_response)
    @api.response(400, 'Invalid input')
    @api.response(404, 'Not found')
    def post(self):
        try:
            review = facade.create_review(api.payload)
            return review.to_dict(), 201
        except ValueError as e:
            if "not found" in str(e).lower():
                api.abort(404, str(e))
            api.abort(400, str(e))

    @api.response(200, 'Success', [review_response])
    def get(self):
        return [r.to_dict() for r in facade.get_all_reviews()], 200

@api.route('/<string:review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Success', review_response)
    @api.response(404, 'Not found')
    def get(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, "Review not found")
        return review.to_dict(), 200

    @api.expect(review_update, validate=True)
    @api.response(200, 'Updated', review_response)
    @api.response(400, 'Invalid input')
    @api.response(404, 'Not found')
    def put(self, review_id):
        try:
            review = facade.update_review(review_id, api.payload)
            if not review:
                api.abort(404, "Review not found")
            return review.to_dict(), 200
        except ValueError as e:
            api.abort(400, str(e))

    @api.response(204, 'Deleted')
    @api.response(404, 'Not found')
    def delete(self, review_id):
        review = facade.delete_review(review_id)
        if not review:
            api.abort(404, "Review not found")
        return '', 204
