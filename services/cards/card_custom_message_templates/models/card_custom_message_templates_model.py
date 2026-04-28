from typing import Optional

from src.models.base import StrictBaseModel


class CardCustomMessageTemplatesModel(StrictBaseModel):
    subjectTemplate: Optional[str] = None
    contentTemplate: Optional[str] = None
