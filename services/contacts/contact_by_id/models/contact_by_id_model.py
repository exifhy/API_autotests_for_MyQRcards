from datetime import datetime
from typing import Any, Optional

from src.models.base import StrictBaseModel


class ContactByIdModel(StrictBaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    transliterateFullName: Optional[str] = None
    email: Optional[str] = None
    mobilePhone: Optional[str] = None
    companyName: Optional[str] = None
    position: Optional[str] = None
    description: Optional[str] = None
    created: Optional[datetime] = None
    modified: Optional[datetime] = None
    accountID: Optional[int] = None
    contactID: Optional[int] = None
    cardID: Optional[int] = None
    avatar: Optional[Any] = None
