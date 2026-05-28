from typing import Optional

from pydantic import BaseModel, ConfigDict


class CardLinkAttributeItemModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: Optional[int] = None
    cardID: Optional[int] = None
    attributeID: Optional[int] = None
    isEnabled: Optional[bool] = None
    values: Optional[list] = None


class CardLinkAttributesModel(BaseModel):
    items: list[CardLinkAttributeItemModel]
