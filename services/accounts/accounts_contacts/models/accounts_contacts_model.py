from datetime import datetime
from typing import Optional

from src.models.base import StrictBaseModel


class AccountContactModel(StrictBaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[str] = None
    mobilePhone: Optional[str] = None
    companyName: Optional[str] = None
    position: Optional[str] = None
    created: Optional[datetime] = None
    accountID: Optional[int] = None
    contactID: Optional[int] = None
