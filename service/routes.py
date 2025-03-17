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
def create_promotions():
    """
    Create a Promotion
    This endpoint will create a Promotion based the data in the body that is posted
    """
    app.logger.info("Request to Create a Promotion...")
    check_content_type("application/json")

    promotion = Promotion()
    # Get the data from the request and deserialize it
    promotion.deserialize(request.get_json())
    promotion.create()
    message = promotion.serialize()
    app.logger.info("Promotion with new id [%s] saved!", promotion.id)

    # Return the location of the new Promotion
    # location_url = url_for("get_promotions", promotion_id=promotion.id, _external=True)
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

######################################################################
# LIST ALL promotions
######################################################################
@app.route("/promotions", methods=["GET"])
def list_promotions():
    """Returns all of the Promotions"""
    app.logger.info("Request for promotion list")

    promotions = []

    # Parse any arguments from the query string
    id = request.args.get("id")
    name = request.args.get("name")

    if id:
        app.logger.info("Find by id: %s", id)
        promotions = Promotion.find(id)
    elif name:
        app.logger.info("Find by name: %s", name)
        promotions = Promotion.find_by_name(name)
    else:
        app.logger.info("Find all")
        promotions = Promotion.all()

    results = [promotion.serialize() for promotion in promotions]
    app.logger.info("Returning %d promotions", len(results))
    return jsonify(results), status.HTTP_200_OK