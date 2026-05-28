from src.models.base import StrictBaseModel


class AccountsCardCatalogCreateItemModel(StrictBaseModel):
    id: int | None = None


class AccountsCardCatalogCreateModel(StrictBaseModel):
    items: list[AccountsCardCatalogCreateItemModel]
