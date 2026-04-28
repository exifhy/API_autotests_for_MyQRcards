from typing import Optional

from pydantic import BaseModel, ConfigDict


class CardLinksStatisticItemModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    accountID: Optional[int] = None
    cardID: Optional[int] = None
    metricTypeID: Optional[int] = None
    metricID: Optional[str] = None
    metricName: Optional[str] = None


class CardLinksStatisticModel(BaseModel):
    items: list[CardLinksStatisticItemModel]
