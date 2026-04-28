from typing import Optional

from src.models.base import StrictBaseModel


class AttachmentV2ItemModel(StrictBaseModel):
    id: Optional[int] = None
    url: Optional[str] = None
    fileName: Optional[str] = None


class AttachmentCreateV2Model(StrictBaseModel):
    attachments: list[AttachmentV2ItemModel] = []
