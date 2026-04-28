from src.models.base import StrictBaseModel


class AccountExistsModel(StrictBaseModel):
    exists: bool

