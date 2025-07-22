from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.amenity import Amenity

class AmenitySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Amenity
        load_instance = True
