from typing import Optional

from src.models.base import StrictBaseModel


class AccountTokenAddModel(StrictBaseModel):
    id: Optional[int] = None
    token: Optional[str] = None
    accountID: Optional[int] = None
    created: Optional[str] = None
    validTill: Optional[str] = None
