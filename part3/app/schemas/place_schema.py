from marshmallow import Schema, fields

class PlaceSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str()
    owner_id = fields.Int(required=True)
    amenities = fields.List(fields.Int(), dump_only=True)
    reviews = fields.List(fields.Int(), dump_only=True)
