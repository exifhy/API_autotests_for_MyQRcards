from typing import Any, Optional

from src.models.base import StrictBaseModel


class AccountsAuthorizePrimaryCardModel(StrictBaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    url: Optional[str] = None
    culture: Optional[str] = None
    isPrimary: Optional[bool] = None
    isHidden: Optional[bool] = None


class AccountsAuthorizeModel(StrictBaseModel):
    accountID: Optional[int] = None
    email: Optional[str] = None
    accountUrl: Optional[str] = None
    isVerified: Optional[bool] = None
    isAcceptAdvertising: Optional[bool] = None
    isCompletedOnboarding: Optional[bool] = None
    primaryCard: Optional[AccountsAuthorizePrimaryCardModel] = None
    userTermsAccepted: Optional[str] = None
    accessJwt: Optional[str] = None
    subscriptions: Optional[list[Any]] = None
