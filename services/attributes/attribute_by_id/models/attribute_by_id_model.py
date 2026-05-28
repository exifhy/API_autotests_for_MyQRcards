from typing import Optional

from src.models.base import StrictBaseModel


class AttributeEntityModel(StrictBaseModel):
    deleted: Optional[str] = None
    name: Optional[str] = None
    id: int


class AttributeTypeModel(StrictBaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    id: int


class AttributeByIdModel(StrictBaseModel):
    attribute: AttributeEntityModel
    type: AttributeTypeModel
    attributeTypeGroupID: Optional[int] = None
    attributeTypeGroupName: Optional[str] = None
    attributeTypeIsPublic: Optional[bool] = None
    selectionModeID: Optional[int] = None
    selectionModeNameRu: Optional[str] = None
    deleted: Optional[str] = None
    modified: Optional[str] = None
