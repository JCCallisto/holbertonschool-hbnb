from flask import jsonify
from marshmallow import ValidationError

def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"msg": "Bad request"}), 400

    @app.errorhandler(401)
    def unauthorized(e):
        return jsonify({"msg": "Unauthorized"}), 401

    @app.errorhandler(403)
    def forbidden(e):
        return jsonify({"msg": "Forbidden"}), 403

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"msg": "Resource not found"}), 404

    @app.errorhandler(422)
    def unprocessable_entity(e):
        return jsonify({"msg": "Unprocessable entity"}), 422

    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify({"msg": "Internal server error"}), 500

    @app.errorhandler(ValidationError)
    def handle_marshmallow_validation(err):
        return jsonify({"errors": err.messages}), 400