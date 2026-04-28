from typing import Optional

from pydantic import BaseModel, ConfigDict


class CardLinksListItemModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    class AccountModel(BaseModel):
        id: Optional[int] = None

    class CardModel(BaseModel):
        id: Optional[int] = None
        name: Optional[str] = None

    class LinkTypeModel(BaseModel):
        id: Optional[int] = None
        name: Optional[str] = None
        isAllowSelfRegistration: Optional[bool] = None

    id: Optional[int] = None
    cardID: Optional[int] = None
    accountID: Optional[int] = None
    name: Optional[str] = None
    url: Optional[str] = None
    account: Optional[AccountModel] = None
    card: Optional[CardModel] = None
    cardLink: Optional[LinkTypeModel] = None


class CardLinksListModel(BaseModel):
    items: list[CardLinksListItemModel]
