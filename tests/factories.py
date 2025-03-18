"""
Test Factory to make fake objects for testing
"""

import factory
from datetime import datetime, timedelta, timezone
from service.models import Promotion


class PromotionFactory(factory.Factory):
    """Creates fake promotions for testing"""

    class Meta:
        model = Promotion

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("first_name")
    promotion_id = factory.Sequence(lambda n: f"PROMO-{n:04d}")
    start_date = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    # Set the end_date to 30 days from now
    end_date = factory.LazyFunction(
        lambda: datetime.now(timezone.utc) + timedelta(days=30)
    )
    promotion_type = factory.Faker("word")
    promotion_amount = factory.Faker(
        "pyfloat", left_digits=2, right_digits=2, positive=True
    )
    promotion_description = factory.Faker("sentence")
