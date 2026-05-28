from typing import Optional

from src.models.base import StrictBaseModel


class AccountsCardWhitelistItemModel(StrictBaseModel):
    allowedAccountID: Optional[int] = None
    accountID: Optional[int] = None
    cardID: Optional[int] = None


class AccountsCardWhitelistsModel(StrictBaseModel):
    items: list[AccountsCardWhitelistItemModel]

