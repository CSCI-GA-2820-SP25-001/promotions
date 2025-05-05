######################################################################
# Copyright 2016, 2024 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################
"""
Module: error_handlers
Centralized Flask error handling.
"""
from http import HTTPStatus

from flask import jsonify
from flask import current_app as app  # Flask application instance

from service.models import DataValidationError

######################################################################
# Error Handlers
######################################################################


@app.errorhandler(DataValidationError)
def request_validation_error(error):
    """Handles validation errors raised by the model layer."""
    return bad_request(error)


@app.errorhandler(HTTPStatus.BAD_REQUEST)
def bad_request(error):
    """400 – Bad Request"""
    message = str(error)
    app.logger.warning(message)
    return (
        jsonify(status=HTTPStatus.BAD_REQUEST, error="Bad Request", message=message),
        HTTPStatus.BAD_REQUEST,
    )


@app.errorhandler(HTTPStatus.NOT_FOUND)
def not_found(error):
    """404 – Resource Not Found"""
    message = str(error)
    app.logger.warning(message)
    return (
        jsonify(status=HTTPStatus.NOT_FOUND, error="Not Found", message=message),
        HTTPStatus.NOT_FOUND,
    )


@app.errorhandler(HTTPStatus.METHOD_NOT_ALLOWED)
def method_not_allowed(error):
    """405 – Method Not Allowed"""
    message = str(error)
    app.logger.warning(message)
    return (
        jsonify(
            status=HTTPStatus.METHOD_NOT_ALLOWED,
            error="Method Not Allowed",
            message=message,
        ),
        HTTPStatus.METHOD_NOT_ALLOWED,
    )


@app.errorhandler(HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
def unsupported_media_type(error):
    """415 – Unsupported Media Type"""
    message = str(error)
    app.logger.warning(message)
    return (
        jsonify(
            status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
            error="Unsupported Media Type",
            message=message,
        ),
        HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
    )


@app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def internal_server_error(error):
    """500 – Internal Server Error"""
    message = str(error)
    app.logger.error(message)
    return (
        jsonify(
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
            error="Internal Server Error",
            message=message,
        ),
        HTTPStatus.INTERNAL_SERVER_ERROR,
    )
