from typing import Optional

from src.models.base import StrictBaseModel


class CardLeadGenFormByIdFieldModel(StrictBaseModel):
    accountID: Optional[int] = None
    cardID: Optional[int] = None
    id: Optional[int] = None
    leadGenFormID: Optional[int] = None
    isVisible: Optional[bool] = None
    isRequired: Optional[bool] = None
    sortOrder: Optional[int] = None
    fieldTemplateID: Optional[int] = None
    customFieldName: Optional[str] = None


class CardLeadGenFormByIdModel(StrictBaseModel):
    fields: list[CardLeadGenFormByIdFieldModel] = []
    accountID: Optional[int] = None
    cardID: Optional[int] = None
    id: Optional[int] = None
    customMessageTemplateID: Optional[int] = None
    formText: Optional[str] = None
    buttonText: Optional[str] = None
