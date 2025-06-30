from flask_restx import Api
from app.api.v1.users import api as users_ns

api = Api(
    version='1.0',
    title='HBnB API',
    description='HBnB Application API'
)

api.add_namespace(users_ns, path='/users')
