from typing import Any

from pydantic import BaseModel, ConfigDict


class SubscriptionListItemModel(BaseModel):
    model_config = ConfigDict(extra="allow")


class SubscriptionListModel(BaseModel):
    items: list[SubscriptionListItemModel]
    raw: list[dict[str, Any]]
