"""
TestPromotion API Service Test Suite – Read Promotion Endpoints
Acceptance Criteria:
1. Given a valid promotion ID, a GET request returns the promotion details.
2. Given an invalid or non-existent promotion ID, a GET request returns a "Promotion Not Found" error.
3. Given a promotion that has expired, a GET request returns the promotion details with a status indicating it is expired.
"""

from datetime import datetime, timedelta, timezone
import os
import logging
from unittest import TestCase
from wsgi import app
from service.common import status
from service.models import db, Promotion
from .factories import PromotionFactory

# Use the DATABASE_URI from config; our docker-compose sets it to the 'postgres' DB
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:pgs3cr3t@postgres:5432/postgres"
)

BASE_URL = "/promotions"


class TestPromotionService(TestCase):
    """Tests for the Read Promotion endpoints"""

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.app_context().push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()

    def setUp(self):
        self.client = app.test_client()
        # Clean out any existing promotions
        db.session.query(Promotion).delete()
        db.session.commit()

    def tearDown(self):
        db.session.remove()

    def _create_promotion(self, promotion_data=None) -> Promotion:
        """
        Helper method to create a promotion via the POST endpoint.
        If promotion_data is provided, use it; otherwise, use the factory defaults.
        """
        if promotion_data is None:
            promotion = PromotionFactory()
        else:
            promotion = PromotionFactory(**promotion_data)
        response = self.client.post(BASE_URL, json=promotion.serialize())
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            "Could not create test promotion",
        )
        new_promotion = response.get_json()
        promotion.id = new_promotion["id"]
        return promotion

    def test_get_expired_promotion(self):
        """
        Given a promotion that has expired, GET /promotions/<id> returns promotion details
        with a status indicating it is expired.
        """
        past_date = datetime.now(timezone.utc) - timedelta(days=1)
        promotion_data = {
            "name": "Expired Promotion",
            "promotion_id": "PROMO-EXPIRED",
            "start_date": (past_date - timedelta(days=10)).isoformat(),
            "end_date": past_date.isoformat(),
            "promotion_type": "discount",
            "promotion_amount": 15.0,
            "promotion_description": "This promotion has expired.",
        }
        promotion = self._create_promotion(promotion_data)
        response = self.client.get(f"{BASE_URL}/{promotion.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(
            data.get("status"),
            "expired",
            "Expected promotion status to be 'expired' for an expired promotion.",
        )

    def test_get_promotion_valid(self):
        """Given a valid promotion ID, GET /promotions/<id> returns promotion details."""
        promotion = self._create_promotion()
        response = self.client.get(f"{BASE_URL}/{promotion.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], promotion.name)
        self.assertEqual(data["promotion_id"], promotion.promotion_id)

    def test_get_promotion_not_found(self):
        """Given a non-existent promotion ID, GET /promotions/<id> returns 404 Not Found."""
        response = self.client.get(f"{BASE_URL}/999999")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        self.assertIn("not found", data["message"].lower())

    def test_index(self):
        """GET / should return 200 OK."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestSadPaths(TestCase):
    """Tests for error handling in the read promotion endpoints"""

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.app_context().push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()

    def setUp(self):
        self.client = app.test_client()

    def test_get_promotion_non_existing_again(self):
        """Another test for a non-existing promotion ID."""
        response = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
