"""
Test Factory to make fake objects for testing
"""

import factory
from service.models import Promotion


class PromotionFactory(factory.Factory):
    """Creates fake pets that you don't have to feed"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Promotion

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("first_name")
    promotion_id = factory.Faker("ean13")
    start_date = factory.Faker("date_time")
    end_date = factory.Faker("date_time")
    promotion_type = factory.Faker("word")
    #Can use an enumeration for promotion type like (BOGO- use a fuzzy choice)
    promotion_amount = factory.Faker("random_number")
    promotion_description = factory.Faker("text")
