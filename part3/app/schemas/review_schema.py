from marshmallow import Schema, fields

class ReviewSchema(Schema):
    id = fields.Int(dump_only=True)
    text = fields.Str(required=True)
    rating = fields.Int()
    place_id = fields.Int(required=True)
    author_id = fields.Int(required=True)
