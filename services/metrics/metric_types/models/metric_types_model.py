from typing import Optional

from src.models.base import StrictBaseModel


class MetricTypeItemModel(StrictBaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    nameRu: Optional[str] = None


class MetricTypesModel(StrictBaseModel):
    items: list[MetricTypeItemModel]

