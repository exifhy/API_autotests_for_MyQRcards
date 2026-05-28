from src.models.base import StrictBaseModel


class AccountsCardCatalogItemsCreateItemModel(StrictBaseModel):
    id: int | None = None


class AccountsCardCatalogItemsCreateModel(StrictBaseModel):
    items: list[AccountsCardCatalogItemsCreateItemModel]
