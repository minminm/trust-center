"""
Module: error_handlers
"""

from flask import current_app as app  # Import Flask application
from pydantic import ValidationError

from app.common.response import make_response
from extension import jwt

from . import status


######################################################################
# Error Handlers
######################################################################
@app.errorhandler(ValidationError)
def handle_validation_error(error):
    msg = str(error)
    app.logger.error(f"Pydantic validation error: %s", msg)
    return make_response(code=status.HTTP_400_BAD_REQUEST, msg=msg)


@app.errorhandler(status.HTTP_400_BAD_REQUEST)
def bad_request(error):
    """Handles bad requests with 400_BAD_REQUEST"""
    msg = str(error)
    app.logger.warning(msg)
    return make_response(code=status.HTTP_400_BAD_REQUEST, msg=msg)


@app.errorhandler(status.HTTP_401_UNAUTHORIZED)
def unorthorized(error):
    """Handles bad requests with 401_UNAUTHORIZED"""
    msg = str(error)
    print(msg)
    app.logger.warning(msg)
    return make_response(code=status.HTTP_401_UNAUTHORIZED, msg=msg)


@app.errorhandler(status.HTTP_404_NOT_FOUND)
def not_found(error):
    """Handles resources not found with 404_NOT_FOUND"""
    msg = str(error)
    app.logger.warning(msg)
    return make_response(code=status.HTTP_404_NOT_FOUND, msg=msg)


@app.errorhandler(status.HTTP_405_METHOD_NOT_ALLOWED)
def method_not_supported(error):
    """Handles unsupported HTTP methods with 405_METHOD_NOT_SUPPORTED"""
    msg = str(error)
    app.logger.warning(msg)
    return make_response(code=status.HTTP_405_METHOD_NOT_ALLOWED, msg=msg)


@app.errorhandler(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
def mediatype_not_supported(error):
    """Handles unsupported media requests with 415_UNSUPPORTED_MEDIA_TYPE"""
    msg = str(error)
    app.logger.warning(msg)
    return make_response(code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, msg=msg)


@app.errorhandler(status.HTTP_500_INTERNAL_SERVER_ERROR)
def internal_server_error(error):
    """Handles unexpected server error with 500_SERVER_ERROR"""
    msg = str(error)
    app.logger.warning(msg)
    return make_response(code=status.HTTP_500_INTERNAL_SERVER_ERROR, msg=msg)


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return make_response(code=status.TOKEN_EXPIRE, msg="Token expired.")


@jwt.unauthorized_loader
def expired_token_callback(error):
    return make_response(code=status.HTTP_401_UNAUTHORIZED, msg="Token missing.")


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return make_response(code=status.HTTP_401_UNAUTHORIZED, msg="Invalid token.")
