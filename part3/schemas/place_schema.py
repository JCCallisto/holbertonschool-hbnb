from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.place import Place

class PlaceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Place
        load_instance = True
