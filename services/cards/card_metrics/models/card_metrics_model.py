from typing import Optional

from src.models.base import StrictBaseModel


class CardMetricItemModel(StrictBaseModel):
    accountID: Optional[int] = None
    cardID: Optional[int] = None
    metricID: Optional[str] = None
    metricTypeID: Optional[int] = None
    metricName: Optional[str] = None
    metricNameRu: Optional[str] = None
    isActive: Optional[bool] = None


class CardMetricsModel(StrictBaseModel):
    items: list[CardMetricItemModel]

