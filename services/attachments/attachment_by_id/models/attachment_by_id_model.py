from typing import Optional

from src.models.base import StrictBaseModel


class AttachmentByIdModel(StrictBaseModel):
    internalFileName: Optional[str] = None
    publicUrl: Optional[str] = None
    created: Optional[str] = None
    deleted: Optional[str] = None
