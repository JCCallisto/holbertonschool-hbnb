from flask_restx import Namespace, Resource

api = Namespace('users', description='User operations')

@api.route('/')
class UserList(Resource):
    
    def get(self):
        return {'message': 'Get all users'}
    
    def post(self):
        return {'message': 'Create user'}

@api.route('/<user_id>')
class User(Resource):
    
    def get(self, user_id):
        return {'message': f'Get user {user_id}'}
    
    def put(self, user_id):
        return {'message': f'Update user {user_id}'}
    
    def delete(self, user_id):
        return {'message': f'Delete user {user_id}'}
