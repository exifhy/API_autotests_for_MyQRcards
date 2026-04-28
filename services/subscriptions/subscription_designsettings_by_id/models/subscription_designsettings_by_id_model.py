from typing import Optional

from src.models.base import StrictBaseModel


class SubscriptionDesignsettingsByIdModel(StrictBaseModel):
    subscriptionID: Optional[int] = None
    accountID: Optional[int] = None
    color: Optional[str] = None
    qrColor: Optional[str] = None
    backgroundColor: Optional[str] = None
    foregroundColor: Optional[str] = None
    backgroundImagePublicUrl: Optional[str] = None
    backgroundAttachmentID: Optional[int] = None
