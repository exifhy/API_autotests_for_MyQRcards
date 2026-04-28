from typing import Optional

from src.models.base import StrictBaseModel


class AccountsSubscriptionHadPremiumModel(StrictBaseModel):
    hasHadPremium: Optional[bool] = None

