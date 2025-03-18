"""
Models for Promotion

All of the models are stored in this module
"""

import logging
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """Used for data validation errors when deserializing"""


class Promotion(db.Model):
    """
    Class that represents a Promotion
    """

    ##################################################
    # Table Schema
    ##################################################
    id = db.Column(db.Integer, primary_key=True)
    promotion_id = db.Column(db.String(63), nullable=False, unique=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    promotion_type = db.Column(db.String(63), nullable=False)
    promotion_amount = db.Column(db.Float, nullable=False)
    promotion_description = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(63), nullable=False)

    def __repr__(self):
        return f"<Promotion {self.name} id=[{self.id}]>"

    def create(self):
        """Creates a Promotion in the database"""
        logger.info("Creating %s", self.name)
        self.id = None  # Ensures new record insertion
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error creating record: %s", self)
            raise DataValidationError(e) from e

    def update(self):
        """Updates a Promotion in the database"""
        logger.info("Updating %s", self.name)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error updating record: %s", self)
            raise DataValidationError(e) from e

    def delete(self):
        """Removes a Promotion from the data store"""
        logger.info("Deleting %s", self.name)
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error deleting record: %s", self)
            raise DataValidationError(e) from e

    def serialize(self) -> dict:
        """Serializes a Promotion into a dictionary"""
        # Allow start_date and end_date to be either datetime or already a string.
        start_date_val = (
            self.start_date.isoformat()
            if hasattr(self.start_date, "isoformat")
            else self.start_date
        )
        end_date_val = (
            self.end_date.isoformat()
            if hasattr(self.end_date, "isoformat")
            else self.end_date
        )
        return {
            "id": self.id,
            "name": self.name,
            "promotion_id": self.promotion_id,
            "start_date": start_date_val,
            "end_date": end_date_val,
            "promotion_type": self.promotion_type,
            "promotion_amount": self.promotion_amount,
            "promotion_description": self.promotion_description,
        }

    def deserialize(self, data):
        """Deserializes a Promotion from a dictionary"""
        try:
            self.name = data["name"]
            self.promotion_id = data["promotion_id"]
            self.start_date = (
                datetime.fromisoformat(data["start_date"])
                if data.get("start_date")
                else None
            )
            self.end_date = (
                datetime.fromisoformat(data["end_date"])
                if data.get("end_date")
                else None
            )
            self.promotion_type = data["promotion_type"]
            self.promotion_amount = data["promotion_amount"]
            self.promotion_description = data["promotion_description"]
        except (AttributeError, KeyError, TypeError) as error:
            raise DataValidationError(f"Invalid attribute: {error}") from error
        return self

    ##################################################
    # CLASS METHODS
    ##################################################

    @classmethod
    def all(cls):
        """Returns all Promotions in the database"""
        logger.info("Fetching all Promotions")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """Finds a Promotion by its ID"""
        logger.info("Fetching Promotion with ID: %s", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_by_name(cls, name):
        """Returns all Promotions with the given name"""
        logger.info("Fetching Promotions with name: %s", name)
        return cls.query.filter(cls.name == name).all()
