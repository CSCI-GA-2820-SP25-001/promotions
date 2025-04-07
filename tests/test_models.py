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
Test cases for Promotion Model
"""

# pylint: disable=duplicate-code
from datetime import datetime
import os
import logging
from unittest import TestCase
from unittest.mock import patch
from wsgi import app
from service.models import Promotion, DataValidationError, db
from .factories import PromotionFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  Promotion   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestPromotion(TestCase):
    """Test Cases for Promotion Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Promotion).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_promotion(self):
        """It should Create a Promotion and assert that it exists"""
        promotion = PromotionFactory()
        promotion.create()
        found = Promotion.all()
        self.assertEqual(len(found), 1)
        data = Promotion.find(promotion.id)
        self.assertEqual(data.id, promotion.id)
        self.assertEqual(data.name, promotion.name)
        self.assertEqual(data.promotion_id, promotion.promotion_id)
        self.assertEqual(data.start_date, promotion.start_date)
        self.assertEqual(data.end_date, promotion.end_date)
        self.assertEqual(data.promotion_type.value, promotion.promotion_type.value)
        self.assertEqual(data.promotion_amount, promotion.promotion_amount)
        self.assertEqual(data.promotion_description, promotion.promotion_description)
        self.assertEqual(data.usage_count, promotion.usage_count)

    def test_serialize_a_promotion(self):
        """It should serialize a Promotion"""
        promotion = PromotionFactory()
        data = promotion.serialize()

        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], promotion.id)
        self.assertIn("name", data)
        self.assertEqual(data["name"], promotion.name)
        self.assertIn("promotion_id", data)
        self.assertEqual(data["promotion_id"], promotion.promotion_id)

        self.assertIn("start_date", data)
        self.assertEqual(data["start_date"], promotion.start_date.isoformat())

        self.assertIn("end_date", data)
        self.assertEqual(data["end_date"], promotion.end_date.isoformat())

        self.assertIn("promotion_type", data)
        self.assertEqual(data["promotion_type"], promotion.promotion_type.value)
        self.assertIn("promotion_amount", data)
        self.assertEqual(data["promotion_amount"], promotion.promotion_amount)
        self.assertIn("promotion_description", data)
        self.assertEqual(data["promotion_description"], promotion.promotion_description)
        self.assertIn("usage_count", data)
        self.assertEqual(data["usage_count"], promotion.usage_count)

    def test_deserialize_a_promotion(self):
        """It should deserialize a Promotion"""
        data = PromotionFactory().serialize()
        promotion = Promotion()
        promotion.deserialize(data)
        print(f"Promotion: {promotion.promotion_amount}, Serialized Data: {data}")
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], promotion.id)
        self.assertIn("name", data)
        self.assertEqual(data["name"], promotion.name)
        self.assertIn("promotion_id", data)
        self.assertEqual(data["promotion_id"], promotion.promotion_id)
        self.assertIn("start_date", data)
        self.assertEqual(
            promotion.start_date, datetime.fromisoformat(data["start_date"])
        )  # Fix
        self.assertIn("end_date", data)
        self.assertEqual(
            promotion.end_date, datetime.fromisoformat(data["end_date"])
        )  # Fix
        self.assertIn("promotion_type", data)
        self.assertEqual(data["promotion_type"], promotion.promotion_type.value)
        self.assertIn("promotion_amount", data)
        self.assertEqual(data["promotion_amount"], promotion.promotion_amount)
        self.assertIn("promotion_description", data)
        self.assertEqual(data["promotion_description"], promotion.promotion_description)
        self.assertIn("usage_count", data)
        self.assertEqual(promotion.usage_count, promotion.usage_count)

    def test_deserialize_missing_data(self):
        """It should not deserialize a Promotion with missing data"""
        data = {
            "name": "Test Promotion",
            "promotion_id": "123456789012",
            "start_date": "2024-01-01T00:00:00Z",
            "end_date": "2024-01-31T00:00:00Z",
        }
        promotion = Promotion()
        self.assertRaises(DataValidationError, promotion.deserialize, data)

    def test_deserialize_bad_data(self):
        """It should not deserialize bad data"""
        data = "this is not a dictionary"
        promotion = Promotion()
        self.assertRaises(DataValidationError, promotion.deserialize, data)

    def test_deserialize_bad_available(self):  # need fix
        """It should not deserialize a bad available attribute"""
        test_promotion = PromotionFactory()
        data = test_promotion.serialize()
        data["promotion_amount"] = "not a number"
        promotion = Promotion()
        self.assertRaises(DataValidationError, promotion.deserialize, data)

    def test_update_a_promotion(self):
        """It should Update a Promotion"""
        promotion = PromotionFactory()
        logging.debug(promotion)
        promotion.create()
        logging.debug(promotion)
        self.assertIsNotNone(promotion.id)

        # Change values and save
        promotion.name = "Updated Promotion Name"
        promotion.promotion_id = "Updated ID"
        promotion.start_date = datetime(2025, 3, 15, 0, 0)
        promotion.end_date = datetime(2025, 3, 20, 0, 0)
        promotion.promotion_type = "DISCOUNT"
        promotion.promotion_amount = 9999
        promotion.promotion_description = "Updated Description"
        promotion.usage_count = 0

        original_id = promotion.id
        promotion.update()

        # Fetch and verify changes
        updated_promotion = Promotion.find(promotion.id)
        self.assertEqual(updated_promotion.id, original_id)
        self.assertEqual(updated_promotion.name, "Updated Promotion Name")
        self.assertEqual(updated_promotion.promotion_id, "Updated ID")
        self.assertEqual(updated_promotion.start_date, datetime(2025, 3, 15, 0, 0))
        self.assertEqual(updated_promotion.end_date, datetime(2025, 3, 20, 0, 0))
        self.assertEqual(updated_promotion.promotion_type.value, "DISCOUNT")
        self.assertEqual(updated_promotion.promotion_amount, 9999)
        self.assertEqual(updated_promotion.promotion_description, "Updated Description")
        self.assertEqual(updated_promotion.usage_count, 0)


class TestExceptionHandlers(TestCase):
    """Promotion Model Exception Handlers"""

    @patch("service.models.db.session.commit")
    def test_create_exception(self, exception_mock):
        """It should catch a create exception"""
        exception_mock.side_effect = Exception()
        promotion = PromotionFactory()
        self.assertRaises(DataValidationError, promotion.create)

    @patch("service.models.db.session.commit")
    def test_update_exception(self, exception_mock):
        """It should catch a update exception"""
        exception_mock.side_effect = Exception()
        promotion = PromotionFactory()
        self.assertRaises(DataValidationError, promotion.update)

    @patch("service.models.db.session.commit")
    def test_delete_exception(self, exception_mock):
        """It should catch a delete exception"""
        exception_mock.side_effect = Exception()
        promotion = PromotionFactory()
        self.assertRaises(DataValidationError, promotion.delete)


class TestModelQueries(TestCase):
    """Promotion Model Query Tests"""

    def test_find_promotion(self):
        """It should Find a Promotion by ID"""
        promotions = PromotionFactory.create_batch(5)
        for promotion in promotions:
            promotion.create()
        logging.debug(promotions)
        # make sure they got saved
        # self.assertEqual(len(Promotion.all()), 5)
        # find the 2nd promotion in the list
        promotion = Promotion.find(promotions[1].id)
        self.assertIsNot(promotion, None)
        self.assertEqual(promotion.id, promotions[1].id)
        self.assertEqual(promotion.name, promotions[1].name)
        self.assertEqual(promotion.promotion_id, promotions[1].promotion_id)
        self.assertEqual(
            promotion.start_date,
            promotions[1].start_date,
        )
        self.assertEqual(
            promotion.end_date,
            promotions[1].end_date,
        )
        self.assertEqual(
            promotion.promotion_type.value,
            promotions[1].promotion_type.value,
        )
        self.assertEqual(
            promotion.promotion_amount,
            promotions[1].promotion_amount,
        )
        self.assertEqual(
            promotion.promotion_description,
            promotions[1].promotion_description,
        )
        self.assertEqual(
            promotion.usage_count,
            promotions[1].usage_count,
        )

    def test_find_by_name(self):
        """It should Find a Promotion by Name"""
        promotions = PromotionFactory.create_batch(10)
        for promotion in promotions:
            promotion.create()
        name = promotions[0].name
        count = len([promotion for promotion in promotions if promotion.name == name])
        found = Promotion.find_by_name(name)
        self.assertEqual(found.count(), count)
        for promotion in found:
            self.assertEqual(promotion.name, name)

    def test_find_by_promotion_type(self):
        """It should Find Promotions by Promotion Type"""
        promotions = PromotionFactory.create_batch(10)
        for promotion in promotions:
            promotion.create()
        promotion_type = promotions[0].promotion_type.value
        count = len(
            [
                promotion
                for promotion in promotions
                if promotion.promotion_type.value == promotion_type
            ]
        )
        found = Promotion.find_by_promotion_type(promotion_type)
        for promotion in found:
            self.assertEqual(promotion.promotion_type.value, promotion_type)
