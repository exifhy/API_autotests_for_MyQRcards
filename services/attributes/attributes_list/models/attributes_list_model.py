from typing import Optional

from src.models.base import StrictBaseModel


class AttributeFeatureModel(StrictBaseModel):
    id: Optional[int] = None
    code: Optional[str] = None


class AttributeListItemModel(StrictBaseModel):
    id: int
    name: Optional[str] = None
    attributeTypeID: Optional[int] = None
    attributeTypeGroupID: Optional[int] = None
    attributeTypeGroupName: Optional[str] = None
    attributeTypeCode: Optional[str] = None
    attributeTypeNameRu: Optional[str] = None
    attributeTypeIsPublic: Optional[bool] = None
    attributeSelectionModeID: Optional[int] = None
    attributeSelectionModeNameRu: Optional[str] = None
    feature: Optional[AttributeFeatureModel] = None


class AttributesListModel(StrictBaseModel):
    items: dict[str, AttributeListItemModel]
