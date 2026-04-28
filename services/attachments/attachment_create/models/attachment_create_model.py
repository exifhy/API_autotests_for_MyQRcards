from typing import Optional

from src.models.base import StrictBaseModel


class AttachmentCreateModel(StrictBaseModel):
    id: Optional[int] = None
    publicUrl: Optional[str] = None
