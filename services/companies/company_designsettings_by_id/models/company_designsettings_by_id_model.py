from typing import Optional

from src.models.base import StrictBaseModel


class CompanyCustomCardLinkModel(StrictBaseModel):
    customCardLinkUrl: Optional[str] = None
    isAttributesSupported: Optional[bool] = None
    name: Optional[str] = None
    id: Optional[int] = None


class CompanyDesignsettingsByIdModel(StrictBaseModel):
    companyID: Optional[int] = None
    accountID: Optional[int] = None
    color: Optional[str] = None
    qrColor: Optional[str] = None
    backgroundColor: Optional[str] = None
    foregroundColor: Optional[str] = None
    backgroundImagePublicUrl: Optional[str] = None
    backgroundAttachmentID: Optional[int] = None
    customCardLink: Optional[CompanyCustomCardLinkModel] = None

