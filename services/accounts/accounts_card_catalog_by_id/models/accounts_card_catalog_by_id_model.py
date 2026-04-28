from pydantic import BaseModel, ConfigDict


class AccountsCardCatalogItemModel(BaseModel):
    model_config = ConfigDict(extra="allow")


class AccountsCardCatalogByIdListModel(BaseModel):
    items: list[AccountsCardCatalogItemModel]
