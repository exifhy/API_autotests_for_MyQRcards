from typing import Optional

from src.models.base import StrictBaseModel


class CompanyEmailSignatureSettingsModel(StrictBaseModel):
    accountID: Optional[int] = None
    companyID: Optional[int] = None
    showGreeting: Optional[bool] = None
    showName: Optional[bool] = None
    showPosition: Optional[bool] = None
    showCompany: Optional[bool] = None
    showPhone: Optional[bool] = None
    showEmail: Optional[bool] = None
    showQR: Optional[bool] = None
    showLogo: Optional[bool] = None
    qrSize: Optional[int] = None
    greetingText: Optional[str] = None
