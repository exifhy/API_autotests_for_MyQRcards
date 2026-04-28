from typing import Optional

from src.models.base import StrictBaseModel


class AttributeTypeGroupItemModel(StrictBaseModel):
    id: int
    name: Optional[str] = None


class AttributeTypeGroupsListModel(StrictBaseModel):
    items: dict[str, AttributeTypeGroupItemModel]
