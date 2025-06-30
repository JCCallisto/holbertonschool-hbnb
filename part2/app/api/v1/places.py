from flask_restx import Namespace, Resource

api = Namespace('places', description='Place operations')

@api.route('/')
class PlaceList(Resource):
    
    def get(self):
        return {'message': 'Get all places'}
    
    def post(self):
        return {'message': 'Create place'}

@api.route('/<place_id>')
class Place(Resource):
    
    def get(self, place_id):
        return {'message': f'Get place {place_id}'}
    
    def put(self, place_id):
        return {'message': f'Update place {place_id}'}
    
    def delete(self, place_id):
        return {'message': f'Delete place {place_id}'}
