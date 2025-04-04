"""
Models for Promotion

All of the models are stored in this module
"""

from datetime import datetime
import logging
import os
from flask_sqlalchemy import SQLAlchemy
from retry import retry
from enum import Enum
from sqlalchemy import Enum as SQLAlchemyEnum

# global variables for retry (must be int)
RETRY_COUNT = int(os.environ.get("RETRY_COUNT", 5))
RETRY_DELAY = int(os.environ.get("RETRY_DELAY", 1))
RETRY_BACKOFF = int(os.environ.get("RETRY_BACKOFF", 2))

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


@retry(
    Exception,
    delay=RETRY_DELAY,
    backoff=RETRY_BACKOFF,
    tries=RETRY_COUNT,
    logger=logger,
)
def init_db() -> None:
    """Initialize Tables"""
    db.create_all()


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""


class PromotionType(Enum):
    """Enumeration of the Promotion types"""

    DISCOUNT = "discount"
    FLASH = "flash"
    COUPON = "coupon"


class Promotion(db.Model):
    """
    Class that represents a Promotion
    """

    ##################################################
    # Table Schema
    ##################################################
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63))
    promotion_id = db.Column(db.String(63), nullable=False, unique=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    promotion_type = db.Column(SQLAlchemyEnum(PromotionType), nullable=False)
    promotion_amount = db.Column(db.Float, nullable=False)
    promotion_description = db.Column(db.String(255), nullable=False)

    # Todo: Place the rest of your schema here...

    def __repr__(self):
        return f"<Promotion {self.name} id=[{self.id}]>"

    def create(self):
        """
        Creates a Promotion to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # pylint: disable=invalid-name
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error creating record: %s", self)
            raise DataValidationError(e) from e

    def update(self):
        """
        Updates a Promotion to the database
        """
        logger.info("Saving %s", self.name)
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
        return {
            "id": self.id,
            "name": self.name,
            "promotion_id": self.promotion_id,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "promotion_type": self.promotion_type.value,
            "promotion_amount": self.promotion_amount,
            "promotion_description": self.promotion_description,
        }

    def deserialize(self, data):
        """
        Deserializes a Promotion from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            if data.get("id") is not None:
                self.id = int(data["id"])
            else:
                self.id = None

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

            self.promotion_type = PromotionType(data["promotion_type"])

            self.promotion_amount = float(data["promotion_amount"])

            self.promotion_description = data["promotion_description"]

        except AttributeError as error:
            raise DataValidationError("Invalid attribute: " + error.args[0]) from error
        except KeyError as error:
            raise DataValidationError(
                "Invalid Promotion: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Promotion: body of request contained bad or no data "
                + str(error)
            ) from error
        except ValueError as error:
            raise DataValidationError(
                "Invalid Promotion: could not convert data - " + str(error)
            ) from error

        return self  # Allow method chaining

    ##################################################
    # CLASS METHODS
    ##################################################

    @classmethod
    def all(cls):
        """Returns all of the Promotions in the database"""
        logger.info("Processing all Promotions")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """Finds a Promotion by it's ID"""
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.session.get(cls, by_id)

    @classmethod
    def find_by_name(cls, name):
        """Returns all Promotions with the given name

        Args:
            name (string): the name of the Promotions you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_promotion_type(cls, promotion_type):
        """
        Returns all Promotions with the given PromotionType
        Args:
            promotion_type (PromotionType): the PromotionType you want to match
        """
        logger.info("Processing promotion_type query for %s ...", promotion_type)
        return cls.query.filter(cls.promotion_type == promotion_type).all()
