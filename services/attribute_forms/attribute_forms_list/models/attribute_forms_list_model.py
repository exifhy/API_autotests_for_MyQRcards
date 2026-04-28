from typing import Optional

from src.models.base import StrictBaseModel


class AttributeFormItemModel(StrictBaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class AttributeFormsListModel(StrictBaseModel):
    items: list[AttributeFormItemModel]
