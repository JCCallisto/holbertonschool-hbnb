from marshmallow import Schema, fields

class AuthSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)
