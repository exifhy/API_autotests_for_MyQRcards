from typing import Optional

from src.models.base import StrictBaseModel


class CardDownloadByIdModel(StrictBaseModel):
    content_type: Optional[str] = None
    is_vcard: bool = False
    body_text: Optional[str] = None
