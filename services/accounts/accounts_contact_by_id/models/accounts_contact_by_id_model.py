from typing import Optional

from src.models.base import StrictBaseModel


class AccountContactByIdModel(StrictBaseModel):
    contactID: int
    cardID: Optional[int] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    transliterateFullName: Optional[str] = None
    email: Optional[str] = None
    mobilePhone: Optional[str] = None
    companyName: Optional[str] = None
    position: Optional[str] = None
    description: Optional[str] = None
    created: Optional[str] = None
    accountID: Optional[int] = None
