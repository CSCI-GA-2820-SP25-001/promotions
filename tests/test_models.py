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

import os
import logging
from unittest import TestCase
from datetime import datetime, timezone
from wsgi import app
from service.models import Promotion, DataValidationError, db
from .factories import PromotionFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  Promotion   M O D E L   T E S T   C A S E S
######################################################################
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

    def test_create_promotion(self):
        """It should create a Promotion"""
        promotion = PromotionFactory()
        promotion.create()
        self.assertIsNotNone(promotion.id)
        found = Promotion.all()
        self.assertEqual(len(found), 1)
        data = Promotion.find(promotion.id)
        self.assertEqual(data.name, promotion.name)

    def test_find_promotion_by_id(self):
        """It should find a Promotion by ID"""
        promotion = PromotionFactory()
        promotion.create()
        found = Promotion.find(promotion.id)
        self.assertIsNotNone(found)
        self.assertEqual(found.id, promotion.id)

    def test_find_promotion_by_name(self):
        """It should find Promotions by Name"""
        promotion = PromotionFactory(name="Black Friday Deal")
        promotion.create()
        results = Promotion.find_by_name("Black Friday Deal")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Black Friday Deal")

    def test_serialize_promotion(self):
        """It should serialize a Promotion"""
        promotion = PromotionFactory()
        serial = promotion.serialize()
        self.assertEqual(serial["id"], promotion.id)
        self.assertEqual(serial["name"], promotion.name)
        self.assertEqual(serial["promotion_id"], promotion.promotion_id)
        self.assertEqual(serial["promotion_type"], promotion.promotion_type)
        self.assertEqual(serial["promotion_amount"], promotion.promotion_amount)
        self.assertEqual(
            serial["promotion_description"], promotion.promotion_description
        )
        self.assertEqual(serial["start_date"], promotion.start_date.isoformat())
        self.assertEqual(serial["end_date"], promotion.end_date.isoformat())

    def test_deserialize_promotion(self):
        """It should deserialize a Promotion"""
        data = {
            "name": "Cyber Monday Sale",
            "promotion_id": "CYBER-MONDAY",
            "start_date": datetime.now(timezone.utc).isoformat(),
            "end_date": (datetime.now(timezone.utc)).isoformat(),
            "promotion_type": "discount",
            "promotion_amount": 20.5,
            "promotion_description": "Limited-time Cyber Monday discount.",
        }
        promotion = Promotion()
        promotion.deserialize(data)
        self.assertEqual(promotion.name, "Cyber Monday Sale")
        self.assertEqual(promotion.promotion_id, "CYBER-MONDAY")
        self.assertEqual(promotion.promotion_type, "discount")
        self.assertEqual(promotion.promotion_amount, 20.5)
        self.assertEqual(
            promotion.promotion_description, "Limited-time Cyber Monday discount."
        )

    def test_deserialize_invalid_data(self):
        """It should raise an error when data is invalid"""
        data = {"name": "Invalid"}
        promotion = Promotion()
        with self.assertRaises(DataValidationError):
            promotion.deserialize(data)

    def test_update_promotion(self):
        """It should update a Promotion"""
        promotion = PromotionFactory()
        promotion.create()
        self.assertIsNotNone(promotion.id)
        promotion.promotion_amount = 50.0
        promotion.update()
        updated = Promotion.find(promotion.id)
        self.assertEqual(updated.promotion_amount, 50.0)

    def test_delete_promotion(self):
        """It should delete a Promotion"""
        promotion = PromotionFactory()
        promotion.create()
        self.assertEqual(len(Promotion.all()), 1)
        promotion.delete()
        self.assertEqual(len(Promotion.all()), 0)

    def test_find_nonexistent_promotion(self):
        """It should return None for a non-existing promotion"""
        result = Promotion.find(9999)
        self.assertIsNone(result)

    def test_repr_method(self):
        """It should return the string representation of a Promotion"""
        promotion = PromotionFactory(name="Holiday Sale")
        self.assertEqual(
            str(promotion), f"<Promotion Holiday Sale id=[{promotion.id}]>"
        )

    def test_find_all_empty(self):
        """It should return an empty list if no Promotions exist"""
        self.assertEqual(len(Promotion.all()), 0)

    def test_deserialize_invalid_dates(self):
        """It should raise an error if the date format is invalid"""
        data = {
            "name": "Invalid Dates",
            "promotion_id": "INVALID-DATE",
            "start_date": "not-a-date",
            "end_date": "still-not-a-date",
            "promotion_type": "discount",
            "promotion_amount": 10.0,
            "promotion_description": "Invalid date test.",
        }
        promotion = Promotion()
        with self.assertRaises(DataValidationError):
            promotion.deserialize(data)

    def test_create_promotion_with_duplicate_promotion_id(self):
        """It should not allow duplicate promotion_id"""
        promotion1 = PromotionFactory(promotion_id="UNIQUE-PROMO")
        promotion1.create()
        promotion2 = PromotionFactory(promotion_id="UNIQUE-PROMO")
        with self.assertRaises(DataValidationError):
            promotion2.create()
