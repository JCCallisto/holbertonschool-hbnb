from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import HBnBFacade

api = Namespace('reviews', description='Review operations')

facade = HBnBFacade()

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, description='Rating from 1 to 5'),
    'place_id': fields.String(required=True, description='ID of the place being reviewed'),
    'user_id': fields.String(required=True, description='ID of the user writing the review')
})

review_response_model = api.model('ReviewResponse', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Review text'),
    'rating': fields.Integer(description='Rating from 1 to 5'),
    'user': fields.Nested(api.model('ReviewUser', {
        'id': fields.String(description='User ID'),
        'first_name': fields.String(description='User first name'),
        'last_name': fields.String(description='User last name')
    })),
    'place': fields.Nested(api.model('ReviewPlace', {
        'id': fields.String(description='Place ID'),
        'title': fields.String(description='Place title')
    })),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})

review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(description='Review text'),
    'rating': fields.Integer(description='Rating from 1 to 5')
})


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created', review_response_model)
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Place or user not found')
    def post(self):
        """Create a new review"""
        try:
            review_data = api.payload
            review = facade.create_review(review_data)
            return review.to_dict(), 201
        except ValueError as e:
            if "not found" in str(e):
                api.abort(404, str(e))
            else:
                api.abort(400, str(e))
        except Exception as e:
            api.abort(400, f"Invalid input data: {str(e)}")

    @api.response(200, 'List of reviews retrieved successfully', [review_response_model])
    def get(self):
        """Get all reviews"""
        try:
            reviews = facade.get_all_reviews()
            return [review.to_dict() for review in reviews], 200
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")


@api.route('/<string:review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully', review_response_model)
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        try:
            review = facade.get_review(review_id)
            if not review:
                api.abort(404, 'Review not found')
            return review.to_dict(), 200
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")

    @api.expect(review_update_model, validate=True)
    @api.response(200, 'Review updated successfully', review_response_model)
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Review not found')
    def put(self, review_id):
        """Update review by ID"""
        try:
            review_data = api.payload
            
            existing_review = facade.get_review(review_id)
            if not existing_review:
                api.abort(404, 'Review not found')
            
            updated_review = facade.update_review(review_id, review_data)
            if not updated_review:
                api.abort(404, 'Review not found')
            
            return updated_review.to_dict(), 200
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(400, f"Invalid input data: {str(e)}")

    @api.response(204, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete review by ID"""
        try:
            deleted = facade.delete_review(review_id)
            if not deleted:
                api.abort(404, 'Review not found')
            return '', 204
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")


@api.route('/places/<string:place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'Reviews for place retrieved successfully', [review_response_model])
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            place = facade.get_place(place_id)
            if not place:
                api.abort(404, 'Place not found')
            
            reviews = [review.to_dict() for review in place.reviews]
            return reviews, 200
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")


@api.route('/users/<string:user_id>/reviews')
class UserReviewList(Resource):
    @api.response(200, 'Reviews by user retrieved successfully', [review_response_model])
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get all reviews written by a specific user"""
        try:
            user = facade.get_user(user_id)
            if not user:
                api.abort(404, 'User not found')
            
            reviews = [review.to_dict() for review in user.reviews]
            return reviews, 200
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")
