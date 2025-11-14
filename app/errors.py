from flask import jsonify
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException


def register_error_handlers(app):

    # ------------------------------
    # Marshmallow Validation Errors
    # ------------------------------
    @app.errorhandler(ValidationError)
    def handle_marshmallow_validation(err):
        return jsonify({
            "error": "Validation Error",
            "messages": err.messages,
            "status": 400
        }), 400

    # ------------------------------
    # HTTP Exceptions (404, 403, 405...)
    # ------------------------------
    @app.errorhandler(HTTPException)
    def handle_http_exceptions(err):
        return jsonify({
            "error": err.name,
            "message": err.description,
            "status": err.code
        }), err.code

    # ------------------------------
    # 500 Internal Server Error
    # ------------------------------
    @app.errorhandler(Exception)
    def handle_general_exception(err):
        print(err)  # You can log this
        return jsonify({
            "error": "Internal Server Error",
            "message": "Something went wrong on our side",
            "status": 500
        }), 500
