from typing import Optional

from src.models.base import StrictBaseModel


class AccountCustomMessageTemplateModel(StrictBaseModel):
    id: Optional[int] = None
    subjectTemplate: Optional[str] = None
    contentTemplate: Optional[str] = None
    accountID: Optional[int] = None
    cardID: Optional[int] = None
    leadGenFormID: Optional[int] = None
    templateID: Optional[int] = None


class AccountsCustomMessageTemplatesModel(StrictBaseModel):
    items: list[AccountCustomMessageTemplateModel]
