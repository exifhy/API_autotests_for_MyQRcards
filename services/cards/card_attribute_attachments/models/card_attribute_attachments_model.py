from typing import Optional

from pydantic import BaseModel, ConfigDict


class CardAttributeAttachmentItemModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: Optional[int] = None
    cardID: Optional[int] = None
    attributeID: Optional[int] = None
    attachmentID: Optional[int] = None
    url: Optional[str] = None


class CardAttributeAttachmentsModel(BaseModel):
    items: list[CardAttributeAttachmentItemModel]
