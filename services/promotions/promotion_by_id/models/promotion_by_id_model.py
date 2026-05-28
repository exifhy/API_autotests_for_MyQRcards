from typing import Optional

from src.models.base import StrictBaseModel


class PromotionByIdModel(StrictBaseModel):
    id: Optional[str] = None
    title: Optional[str] = None
    message: Optional[str] = None
    additionalMessage: Optional[str] = None
    grantSubscriptionID: Optional[int] = None
    grantPeriodDays: Optional[int] = None
    dateFrom: Optional[str] = None
    dateTill: Optional[str] = None
    isForNewAccount: Optional[bool] = None
    isForFreeAccount: Optional[bool] = None
    isForPayedAccount: Optional[bool] = None
    isForEnterpriseAccount: Optional[bool] = None

