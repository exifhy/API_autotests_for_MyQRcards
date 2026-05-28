from typing import Optional

from src.models.base import StrictBaseModel


class AttachmentDeleteByIdModel(StrictBaseModel):
    status_code: Optional[int] = None
