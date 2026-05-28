from datetime import datetime
from typing import Optional

from src.models.base import StrictBaseModel


class SuccessAccountAddResultEntityModel(StrictBaseModel):
    isPasswordDefined: Optional[bool] = None
    isNewAccount: Optional[bool] = None
    id: Optional[int] = None
    verificationRequestValidTill: Optional[datetime] = None
    isEmailVerified: Optional[bool] = None
    isMobilePhoneVerified: Optional[bool] = None
