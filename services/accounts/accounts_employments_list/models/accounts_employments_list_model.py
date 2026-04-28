from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class AccountsEmploymentCompanyModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: Optional[int] = None
    name: Optional[str] = None


class AccountsEmploymentItemModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    accountID: Optional[int] = None
    cardID: Optional[int] = None
    defaultCardLinkID: Optional[str] = None
    defaultCardLinkUrl: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    mobilePhone: Optional[str] = None
    position: Optional[str] = None
    company: Optional[AccountsEmploymentCompanyModel] = None


class AccountsEmploymentsListModel(BaseModel):
    items: list[AccountsEmploymentItemModel]
    raw: list[dict[str, Any]]
