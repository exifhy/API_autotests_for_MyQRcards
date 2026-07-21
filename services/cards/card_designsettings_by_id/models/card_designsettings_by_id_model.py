from typing import Optional

from src.models.base import StrictBaseModel


class CardDesignsettingsCustomCardLinkModel(StrictBaseModel):
    customCardLinkUrl: Optional[str] = None
    isAttributesSupported: Optional[bool] = None
    name: Optional[str] = None
    id: Optional[int] = None


class CardDesignsettingsFontStyleModel(StrictBaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    fontFamily: Optional[str] = None
    url: Optional[str] = None


class CardDesignsettingsByIdModel(StrictBaseModel):
    cardID: Optional[int] = None
    accountID: Optional[int] = None
    color: Optional[str] = None
    qrColor: Optional[str] = None
    backgroundColor: Optional[str] = None
    foregroundColor: Optional[str] = None
    backgroundImagePublicUrl: Optional[str] = None
    backgroundAttachmentID: Optional[int] = None
    customCardLink: Optional[CardDesignsettingsCustomCardLinkModel] = None
    fontColor: Optional[str] = None
    fontStyle: Optional[CardDesignsettingsFontStyleModel] = None

