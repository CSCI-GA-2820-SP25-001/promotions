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
from datetime import timezone
import os
import logging
from unittest import TestCase
from wsgi import app
from service.common import status
from service.models import db, Promotion
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
        self.assertEqual(new_promotion["name"], test_promotion.name)
        self.assertEqual(new_promotion["promotion_id"], test_promotion.promotion_id)
        self.assertEqual(
            parsedate_to_datetime(new_promotion["start_date"]).replace(microsecond=0),
            test_promotion.start_date.replace(tzinfo=timezone.utc, microsecond=0),
        )
        self.assertEqual(
            parsedate_to_datetime(new_promotion["end_date"]).replace(microsecond=0),
            test_promotion.end_date.replace(tzinfo=timezone.utc, microsecond=0),
        )
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
