from flask_restx import Namespace, Resource

api = Namespace('reviews', description='Review operations')

@api.route('/')
class ReviewList(Resource):
    
    def get(self):
        return {'message': 'Get all reviews'}
    
    def post(self):
        return {'message': 'Create review'}

@api.route('/<review_id>')
class Review(Resource):
    
    def get(self, review_id):
        return {'message': f'Get review {review_id}'}
    
    def put(self, review_id):
        return {'message': f'Update review {review_id}'}
    
    def delete(self, review_id):
        return {'message': f'Delete review {review_id}'}
