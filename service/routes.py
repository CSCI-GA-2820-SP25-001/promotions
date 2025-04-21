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
from service.models import Promotion, PromotionType
from service.common import status  # HTTP Status Codes


############################################################
# Health Endpoint
############################################################
@app.route("/health")
def health():
    """Health Status"""
    return jsonify(status="OK"), 200


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response with API metadata"""
    return app.send_static_file("index.html")


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


@app.route("/promotions/<int:promotion_id>", methods=["DELETE"])
def delete_promotions(promotion_id):
    """
    Delete a Promotion

    This endpoint will delete a Promotion based the id specified in the path
    """
    app.logger.info("Request to Delete a promotion with id [%s]", promotion_id)

    # Delete the Promotion if it exists
    promotion = Promotion.find(promotion_id)
    if promotion:
        app.logger.info("Promotion with ID: %d found.", promotion.id)
        promotion.delete()

    app.logger.info("Promotion with ID: %d delete complete.", promotion_id)
    return {}, status.HTTP_204_NO_CONTENT


@app.route("/promotions/<int:promotion_id>", methods=["GET"])
def get_promotions(promotion_id):
    """
    Retrieve a single Promotion

    This endpoint will return a Promotion based on its id
    """
    app.logger.info("Request to Retrieve a promotion with id [%s]", promotion_id)

    # Attempt to find the Promotion and abort if not found
    promotion = Promotion.find(promotion_id)
    if not promotion:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Promotion with id '{promotion_id}' was not found.",
        )

    app.logger.info("Returning promotion: %s", promotion.name)
    return jsonify(promotion.serialize()), status.HTTP_200_OK


@app.route("/promotions/<int:promotion_id>", methods=["PUT"])
def update_promotion(promotion_id):
    """
    Update an existing Promotion
    """
    app.logger.info("Request to update Promotion with id: %s", promotion_id)
    check_content_type("application/json")

    promotion = Promotion.find(promotion_id)
    if not promotion:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Promotion with id '{promotion_id}' was not found.",
        )

    promotion.deserialize(request.get_json())
    promotion.update()

    return jsonify(promotion.serialize()), status.HTTP_200_OK


@app.route("/promotions/<int:promotion_id>/apply", methods=["PUT"])
def apply_promotion(promotion_id):
    """
    Applies a promotion and increments its usage count
    """
    app.logger.info(f"Request to apply promotion with id: {promotion_id}")
    promotion = Promotion.find(promotion_id)
    if not promotion:
        abort(404, description=f"Promotion with id {promotion_id} not found")

    promotion.usage_count += 1
    promotion.update()

    return jsonify(promotion.serialize()), 200


######################################################################
# LIST ALL promotions
######################################################################
@app.route("/promotions", methods=["GET"])
def list_promotions():
    """Returns all of the Promotions or filters by query parameters"""
    app.logger.info("Request for promotion list")

    allowed_params = {"promotion_id", "name", "promotion_type"}
    for key in request.args.keys():
        if key not in allowed_params:
            abort(400, description=f"Invalid query parameter: {key}")

    query = Promotion.query

    promotion_id = request.args.get("promotion_id")
    name = request.args.get("name")
    promotion_type_param = request.args.get("promotion_type")

    if promotion_id:
        app.logger.info("Filter by promotion_id: %s", promotion_id)
        query = query.filter(Promotion.promotion_id == str(promotion_id))

    if name:
        app.logger.info("Filter by name: %s", name)
        query = query.filter(Promotion.name == name)

    if promotion_type_param:
        try:
            promotion_type_enum = PromotionType(promotion_type_param)
            query = query.filter(Promotion.promotion_type == promotion_type_enum)
        except ValueError:
            abort(400, description=f"Invalid promotion_type: {promotion_type_param}")

    promotions = query.all()
    results = [promotion.serialize() for promotion in promotions]
    app.logger.info("Returning %d promotions", len(results))
    return jsonify(results), status.HTTP_200_OK


######################################################################
# CANCEL A PROMOTION (STATEFUL ACTION)
######################################################################
@app.route("/promotions/<int:promotion_id>/cancel", methods=["PUT"])
def cancel_promotion(promotion_id):
    """Cancel a Promotion by changing its state to 'canceled'"""
    app.logger.info("Request to cancel promotion with id: %d", promotion_id)

    # Find the promotion
    promotion = Promotion.find(promotion_id)
    if not promotion:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Promotion with id '{promotion_id}' was not found.",
        )

    # Only cancel if currently active
    if promotion.state != "active":
        abort(
            status.HTTP_409_CONFLICT,
            f"Promotion with id '{promotion_id}' cannot be canceled because it is not active.",
        )

    # Perform the state change
    promotion.state = "canceled"
    promotion.update()

    app.logger.info("Promotion with ID: %d has been canceled.", promotion_id)
    return jsonify(promotion.serialize()), status.HTTP_200_OK
