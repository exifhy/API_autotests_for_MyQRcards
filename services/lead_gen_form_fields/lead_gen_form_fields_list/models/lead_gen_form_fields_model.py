from typing import Optional

from src.models.base import StrictBaseModel


class LeadGenFormFieldModel(StrictBaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    nameRu: Optional[str] = None
    nameEn: Optional[str] = None
