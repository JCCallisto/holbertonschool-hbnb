from flask_restx import Namespace, Resource, fields

from business.facade import hbnb_facade

api = Namespace('reviews', description="Review operations")

review_model = api.model('Review', {
    'id': fields.String(readonly=True),
    'text': fields.String(required=True),
    'user_id': fields.String(required=True),
    'place_id': fields.String(required=True),
    'created_at': fields.String,
    'updated_at': fields.String,
})

review_create = api.model('ReviewCreate', {
    'text': fields.String(required=True),
    'user_id': fields.String(required=True),
    'place_id': fields.String(required=True),
})

review_update = api.model('ReviewUpdate', {
    'text': fields.String,
})

@api.route('/')
class ReviewList(Resource):
    @api.marshal_list_with(review_model)
    def get(self):
        return hbnb_facade.list_reviews()

    @api.expect(review_create)
    @api.marshal_with(review_model, code=201)
    def post(self):
        data = api.payload
        return hbnb_facade.create_review(data), 201

@api.route('/<string:review_id>')
class ReviewResource(Resource):
    @api.marshal_with(review_model)
    def get(self, review_id):
        return hbnb_facade.get_review(review_id)

    @api.expect(review_update)
    @api.marshal_with(review_model)
    def put(self, review_id):
        data = api.payload
        return hbnb_facade.update_review(review_id, data)

    def delete(self, review_id):
        hbnb_facade.delete_review(review_id)
        return {"message": "Review deleted"}, 204
