from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CodeMessageModel(StrictBaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(StrictBaseModel):
    list_model: List[CodeMessageModel]


class UserDisabledNotificationsModel(StrictBaseModel):
    providerID: int
    isOn: bool


class UserDisabledNotificationsListResponseModel(StrictBaseModel):
    results: List[UserDisabledNotificationsModel]
