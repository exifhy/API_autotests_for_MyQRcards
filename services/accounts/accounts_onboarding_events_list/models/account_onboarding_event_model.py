from typing import Optional

from src.models.base import StrictBaseModel


class AccountOnboardingEventModel(StrictBaseModel):
    accountID: Optional[int] = None
    typeID: Optional[int] = None
    code: Optional[str] = None
    nameRu: Optional[str] = None
    created: Optional[str] = None
