from typing import Optional

from src.models.base import StrictBaseModel


class AttributeTypeGroupModel(StrictBaseModel):
    name: Optional[str] = None
    id: Optional[int] = None


class AttributeTypeItemModel(StrictBaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    isPublic: Optional[bool] = None
    attributeTypeGroup: Optional[AttributeTypeGroupModel] = None


class AttributeTypesListModel(StrictBaseModel):
    items: dict[str, AttributeTypeItemModel]
