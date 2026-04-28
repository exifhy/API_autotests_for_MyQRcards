from typing import Optional

from pydantic import BaseModel, ConfigDict


class CardAttributeAttachmentUploadItemModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: Optional[int] = None
    url: Optional[str] = None
    fileName: Optional[str] = None


class CardAttributeAttachmentUploadModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    items: list[CardAttributeAttachmentUploadItemModel] = []
    attachments: list[CardAttributeAttachmentUploadItemModel] = []
