from typing import Optional

from src.models.base import StrictBaseModel


class AccountListItemModel(StrictBaseModel):
    id: Optional[int] = None
    email: Optional[str] = None


class AccountsListModel(StrictBaseModel):
    items: list[AccountListItemModel]
