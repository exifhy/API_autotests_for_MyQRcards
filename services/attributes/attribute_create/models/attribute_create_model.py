from typing import Optional

from src.models.base import StrictBaseModel


class AttributeCreateModel(StrictBaseModel):
    id: int
    name: Optional[str] = None
    attributeTypeID: Optional[int] = None
    attributeTypeGroupID: Optional[int] = None
