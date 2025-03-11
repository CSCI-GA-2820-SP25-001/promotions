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
import os
import logging
import datetime
from unittest import TestCase
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
        self.assertIsNotNone(promotion.id)
        found = Promotion.all()
        self.assertEqual(len(found), 1)
        data = Promotion.find(promotion.id)
        self.assertEqual(data.id, promotion.id)
        self.assertEqual(data.name, promotion.name)
        self.assertEqual(data.promotion_id, promotion.promotion_id)
        self.assertEqual(data.start_date, promotion.start_date)
        self.assertEqual(data.end_date, promotion.end_date)
        self.assertEqual(data.promotion_type, promotion.promotion_type)
        self.assertEqual(data.promotion_amount, promotion.promotion_amount)
        self.assertEqual(data.promotion_description, promotion.promotion_description)
    
    def test_update_a_promotion(self):
        """It should Update a Promotion"""
        promotion = PromotionFactory()
        logging.debug(promotion)
        promotion.create()
        logging.debug(promotion)
        self.assertIsNotNone(promotion.id)
        # Change it an save it
        promotion.name = "some_new_promotion_name"
        promotion.promotion_id = "some_new_promotion_promotion_id"
        new_date = datetime.datetime(1920, 1, 25, 0,0)
        promotion.start_date = new_date
        promotion.end_date = new_date
        promotion.promotion_type = "some_new_promotion_type"
        promotion.promotion_amount = 9999
        promotion.promotion_description = "some_new_promotion_description"
        original_id = promotion.id
        promotion.update()
         # Fetch it back and make sure the id hasn't changed
        # but the data did change
        new_promotion = Promotion.find(promotion.id)
        self.assertEqual(new_promotion.id, original_id)
        self.assertEqual(new_promotion.name, "some_new_promotion_name")
        self.assertEqual(new_promotion.promotion_id, "some_new_promotion_promotion_id")
        self.assertEqual(new_promotion.start_date, new_date)
        self.assertEqual(new_promotion.end_date, new_date)
        self.assertEqual(new_promotion.promotion_type, "some_new_promotion_type")
        self.assertEqual(new_promotion.promotion_amount, 9999)
        self.assertEqual(new_promotion.promotion_description, "some_new_promotion_description")
       
