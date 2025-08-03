from marshmallow import Schema, fields, validate

class PlaceSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1))
    description = fields.Str()
    price = fields.Float(required=True)
    location = fields.Str()
    latitude = fields.Float()
    longitude = fields.Float()

class ReviewSchema(Schema):
    comment = fields.Str(required=True, validate=validate.Length(min=1))
    rating = fields.Int(required=True, validate=validate.Range(min=1, max=5))
