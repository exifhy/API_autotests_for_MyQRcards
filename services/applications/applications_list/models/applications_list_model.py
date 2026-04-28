from typing import Optional

from src.models.base import StrictBaseModel


class ApplicationItemModel(StrictBaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class ApplicationsListModel(StrictBaseModel):
    items: list[ApplicationItemModel]
