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
from service.models import DataValidationError, db, Promotion
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
        self.assertEqual(new_promotion["promotion_type"], test_promotion.promotion_type)
        self.assertEqual(
            new_promotion["promotion_amount"], test_promotion.promotion_amount
        )
        self.assertEqual(
            new_promotion["promotion_description"], test_promotion.promotion_description
        )

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

     ######################################################################
    # Sad Path 3: Non-existent Name
    ######################################################################
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
