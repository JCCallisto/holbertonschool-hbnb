from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.review import Review

class ReviewSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Review
        load_instance = True
