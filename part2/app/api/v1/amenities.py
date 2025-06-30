from flask_restx import Namespace, Resource

api = Namespace('amenities', description='Amenity operations')

@api.route('/')
class AmenityList(Resource):
    
    def get(self):
        return {'message': 'Get all amenities'}
    
    def post(self):
        return {'message': 'Create amenity'}

@api.route('/<amenity_id>')
class Amenity(Resource):
    
    def get(self, amenity_id):
        return {'message': f'Get amenity {amenity_id}'}
    
    def put(self, amenity_id):
        return {'message': f'Update amenity {amenity_id}'}
    
    def delete(self, amenity_id):
        return {'message': f'Delete amenity {amenity_id}'}
