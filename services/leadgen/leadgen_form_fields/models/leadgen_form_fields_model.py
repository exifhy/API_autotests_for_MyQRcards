from typing import Optional

from src.models.base import StrictBaseModel


class LeadGenFormFieldItemModel(StrictBaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    nameRu: Optional[str] = None
    nameEn: Optional[str] = None


class LeadGenFormFieldsModel(StrictBaseModel):
    items: list[LeadGenFormFieldItemModel]

