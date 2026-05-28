from typing import Optional

from src.models.base import StrictBaseModel


class CardLinkMetricItemModel(StrictBaseModel):
    accountID: Optional[int] = None
    cardID: Optional[int] = None
    metricID: Optional[str] = None
    metricTypeID: Optional[int] = None
    metricName: Optional[str] = None
    metricNameRu: Optional[str] = None
    isActive: Optional[bool] = None


class CardLinkMetricsModel(StrictBaseModel):
    items: list[CardLinkMetricItemModel]

