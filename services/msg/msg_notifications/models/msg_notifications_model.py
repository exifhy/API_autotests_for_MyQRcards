from typing import Optional, Dict, List, Any
from pydantic import BaseModel, RootModel, ConfigDict, Field
from datetime import datetime


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class NotificationListResult(StrictBaseModel):
    id: int
    providerID: int
    subject: Optional[str] = None
    content: Optional[str] = None
    contentTypeID: Optional[int] = None
    created: datetime
    sent: Optional[datetime] = None
    navigateTo: Optional[int] = None
    taskID: Optional[int] = None
    isViewed: bool


class NotificationListResultModel(RootModel):
    root: Dict[str, NotificationListResult]
