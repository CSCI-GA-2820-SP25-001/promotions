"""
Test Factory to make fake objects for testing
"""

import random
from datetime import timedelta

import factory
import factory.random
from service.models import Promotion, PromotionType


class PromotionFactory(factory.Factory):
    """Creates fake promotions that you don't have to feed"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Promotion

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("first_name")
    promotion_id = factory.Faker("ean8")
    start_date = factory.Faker("date_time")

    @factory.lazy_attribute
    def end_date(self):
        """Generates an end_date 7 days after start_date"""
        return self.start_date + timedelta(days=7)

    promotion_type = factory.LazyFunction(lambda: random.choice(list(PromotionType)))
    promotion_amount = factory.Faker("random_number")
    promotion_description = factory.Faker("text")
    usage_count = factory.Faker("random_int", min=0, max=100)
