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
TestPromotion API Service Test Suite
TestPromotion API Service Test Suite
"""

# pylint: disable=duplicate-code
from datetime import datetime, timezone
import os
import logging
from unittest import TestCase
from unittest.mock import MagicMock, patch
from wsgi import app
from service.common import status
from service.models import DataValidationError, PromotionType, db, Promotion
from .factories import PromotionFactory
from email.utils import parsedate_to_datetime

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)

BASE_URL = "/promotions"


######################################################################
#  T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestPromotionService(TestCase):
    """REST API Server Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()
        db.session.query(Promotion).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    def _create_promotions(self, count: int = 1) -> list:
        """Factory method to create promotions in bulk"""
        promotions = []
        for _ in range(count):
            test_promotion = PromotionFactory()
            response = self.client.post(BASE_URL, json=test_promotion.serialize())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test promotion",
            )
            new_promotion = response.get_json()
            test_promotion.id = new_promotion["id"]
            promotions.append(test_promotion)
        return promotions

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """It should call the home page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_promotion(self):
        """It should Create a new Promotion"""
        test_promotion = PromotionFactory()
        logging.debug("Test Promotion: %s", test_promotion.serialize())
        response = self.client.post(BASE_URL, json=test_promotion.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_promotion = response.get_json()

        print(f"Raw start_date from API: {new_promotion['start_date']}")

        self.assertEqual(new_promotion["name"], test_promotion.name)
        self.assertEqual(new_promotion["promotion_id"], test_promotion.promotion_id)
        received_start_date = (
            datetime.fromisoformat(new_promotion["start_date"])
            .astimezone(timezone.utc)
            .replace(microsecond=0)
        )
        expected_start_date = test_promotion.start_date.astimezone(
            timezone.utc
        ).replace(microsecond=0)
        self.assertEqual(received_start_date, expected_start_date)

        received_end_date = (
            datetime.fromisoformat(new_promotion["end_date"])
            .astimezone(timezone.utc)
            .replace(microsecond=0)
        )
        expected_end_date = test_promotion.end_date.astimezone(timezone.utc).replace(
            microsecond=0
        )
        self.assertEqual(received_end_date, expected_end_date)
        self.assertEqual(
            new_promotion["promotion_type"], test_promotion.promotion_type.value
        )
        self.assertEqual(
            new_promotion["promotion_amount"], test_promotion.promotion_amount
        )
        self.assertEqual(
            new_promotion["promotion_description"], test_promotion.promotion_description
        )

    def test_delete_promotions(self):
        """It should Delete a Promotion"""
        test_promotions = self._create_promotions(1)[0]
        response = self.client.delete(f"{BASE_URL}/{test_promotions.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(response.data), 0)
        # make sure they are deleted
        response = self.client.get(f"{BASE_URL}/{test_promotions.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_non_existing_promotions(self):
        """It should Delete a Promotion even if it doesn't exist"""
        response = self.client.delete(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(response.data), 0)

    def test_get_promotion_not_found(self):
        """Given a non-existent promotion ID, GET /promotions/<id> returns 404 Not Found."""
        response = self.client.get(f"{BASE_URL}/999999")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        self.assertIn("not found", data.get("message", "").lower())

    def test_get_valid_promotion(self):
        """Given a valid promotion ID, GET /promotions/<id> returns promotion details."""
        test_promotions = self._create_promotions(1)
        promotion = test_promotions[0]
        response = self.client.get(f"{BASE_URL}/{promotion.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data.get("name"), promotion.name)
        self.assertEqual(data.get("promotion_id"), promotion.promotion_id)

        # Check that the location header was correct
        # response = self.client.get(location)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # new_promotion = response.get_json()
        # self.assertEqual(new_promotion["name"], test_promotion.name)
        # self.assertEqual(new_promotion["address"], test_promotion.address)
        # self.assertEqual(new_promotion["email"], test_promotion.email)

    def test_get_promotion_list(self):
        """It should Get a list of promotion"""
        self._create_promotions(5)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertIsInstance(data, list)

    def test_query_by_promotion_type(self):
        """It should return a list of promotions filtered by promotion_type"""
        # Create random promotions
        self._create_promotions(3)

        # Add at least one known 'discount' promotion
        discount_promo = PromotionFactory(promotion_type=PromotionType.DISCOUNT)
        response = self.client.post(BASE_URL, json=discount_promo.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        discount_promo.id = response.get_json()["id"]

        # Send the query
        response = self.client.get(f"{BASE_URL}?promotion_type=DISCOUNT")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertIsInstance(data, list)

        # All returned promotions should be 'discount'
        for promo in data:
            self.assertEqual(promo["promotion_type"], "DISCOUNT")

    def test_query_by_multiple_fields(self):
        """It should return promotions filtered by promotion_type and name"""
        # Create known promotion
        promo = PromotionFactory(promotion_type=PromotionType.DISCOUNT, name="TEST1")
        response = self.client.post(BASE_URL, json=promo.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Create another promotion with different name
        promo2 = PromotionFactory(promotion_type=PromotionType.DISCOUNT, name="TEST2")
        self.client.post(BASE_URL, json=promo2.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Query with two filters
        response = self.client.get(f"{BASE_URL}?promotion_type=DISCOUNT&name=TEST1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "TEST1")
        self.assertEqual(data[0]["promotion_type"].upper(), "DISCOUNT")

    def test_query_by_non_existent_field(self):
        """
        It should return an empty list when querying by a non-existent field.
        """
        # Create a promotion
        self._create_promotions(1)

        # Query by a non-existent field
        response = self.client.get(f"{BASE_URL}?non_existent_field=value")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestSadPaths(TestCase):
    """Test REST Exception Handling"""

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()

    def test_method_not_allowed(self):
        """It should not allow update without a promotion id"""
        response = self.client.put(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_promotion_no_data(self):
        """It should not Create a Promotion with missing data"""
        response = self.client.post(BASE_URL, json={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_promotion_no_content_type(self):
        """It should not Create a Promotion with no content type"""
        response = self.client.post(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_promotion_wrong_content_type(self):
        """It should not Create a Promotion with the wrong content type"""
        response = self.client.post(BASE_URL, data="hello", content_type="text/html")
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_error_404(self):
        """It should not find a Promotion that is not there"""
        response = self.client.get("/promotions/0")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Not Found", str(response.data))

    # Add this
    def test_update_promotion(self):
        """It should Update an existing Promotion"""
        # Create a promotion first
        test_promotion = PromotionFactory()
        response = self.client.post(BASE_URL, json=test_promotion.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Modify the promotion data
        new_promotion = response.get_json()
        logging.debug(new_promotion)
        new_promotion["name"] = "Updated Promotion Name"
        new_promotion["promotion_amount"] = 9999
        new_promotion["promotion_type"] = "DISCOUNT"
        new_promotion["promotion_description"] = "Updated Description"

        # Send an update request
        response = self.client.put(
            f"{BASE_URL}/{new_promotion['id']}", json=new_promotion
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the response
        updated_promotion = response.get_json()
        self.assertEqual(updated_promotion["name"], "Updated Promotion Name")
        self.assertEqual(updated_promotion["promotion_amount"], 9999)
        self.assertEqual(updated_promotion["promotion_type"], "DISCOUNT")
        self.assertEqual(
            updated_promotion["promotion_description"], "Updated Description"
        )

    def test_get_promotion_list_non_existent_name(self):
        """
        It should return a 200 with an empty list if the requested name doesn't exist.
        (Current code doesn't raise a 404 if the name is not found.)
        """
        response = self.client.get(f"{BASE_URL}?name=NoSuchNameExists")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 0, "Expected an empty list for a non-existent name")

    ######################################################################
    #  T E S T   M O C K S
    ######################################################################

    # @patch("service.routes.Promotion.find_by_name")
    # def test_bad_request(self, bad_request_mock):
    #     """It should return a Bad Request error from Find By Name"""
    #     bad_request_mock.side_effect = DataValidationError()
    #     response = self.client.get(BASE_URL, query_string="name=fido")
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # @patch("service.routes.Promotion.find_by_name")
    # def test_mock_search_data(self, promotion_find_mock):
    #     """It should showing how to mock data"""
    #     promotion_find_mock.return_value = [
    #         MagicMock(serialize=lambda: {"name": "fido"})
    #     ]
    #     response = self.client.get(BASE_URL, query_string="name=fido")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
