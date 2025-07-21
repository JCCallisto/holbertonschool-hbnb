from flask import Flask
from flask_restx import Api

app = Flask(__name__)
api = Api(app, version="1.0", title="HBnB API", description="HBnB Evolution Project API")

# Import and add namespaces
from api.v1.users import api as users_ns
from api.v1.amenities import api as amenities_ns
from api.v1.places import api as places_ns
from api.v1.reviews import api as reviews_ns

api.add_namespace(users_ns, path="/api/v1/users")
api.add_namespace(amenities_ns, path="/api/v1/amenities")
api.add_namespace(places_ns, path="/api/v1/places")
api.add_namespace(reviews_ns, path="/api/v1/reviews")

if __name__ == "__main__":
    app.run(debug=True)
