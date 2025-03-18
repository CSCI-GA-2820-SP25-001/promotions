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
Promotion Service

This service implements a REST API that allows you to Create, Read, Update
and Delete Promotion
"""

from flask import jsonify, request, url_for, abort
from flask import current_app as app  # Import Flask application
from service.models import Promotion
from service.common import status  # HTTP Status Codes
from datetime import datetime, timezone


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return (
        "Reminder: return some useful information in json format about the service here",
        status.HTTP_200_OK,
    )


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################


@app.route("/promotions", methods=["POST"])
def create_promotion():
    """
    Create a Promotion
    This endpoint will create a Promotion based on the data in the body that is posted.
    """
    app.logger.info("Request to Create a Promotion...")
    check_content_type("application/json")

    promotion = Promotion()
    # Get the data from the request and deserialize it.
    promotion.deserialize(request.get_json())
    promotion.create()
    message = promotion.serialize()
    app.logger.info("Promotion with new id [%s] saved!", promotion.id)

    # Return the location of the new Promotion.
    location_url = "unknown"

    return (
        jsonify(message),
        status.HTTP_201_CREATED,
        {"Location": location_url},
    )


def check_content_type(content_type) -> None:
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )


def error(status_code, reason):
    app.logger.error(reason)
    abort(status_code, reason)


@app.route("/promotions/<int:promotion_id>", methods=["GET"])
def get_promotions(promotion_id):
    """
    Retrieve a single Promotion.
    This endpoint returns a Promotion based on its id.
    If the promotion's end_date is in the past, a "status": "expired" field is added to the returned JSON.
    """
    app.logger.info("Request to Retrieve a promotion with id [%s]", promotion_id)
    promotion = Promotion.find(promotion_id)
    if not promotion:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Promotion with id '{promotion_id}' was not found.",
        )
    promotion_data = promotion.serialize()
    # Ensure promotion.end_date is timezone-aware.
    end_date = promotion.end_date
    if end_date.tzinfo is None:
        end_date = end_date.replace(tzinfo=timezone.utc)
    if end_date < datetime.now(timezone.utc):
        promotion_data["status"] = "expired"
    return jsonify(promotion_data), status.HTTP_200_OK
