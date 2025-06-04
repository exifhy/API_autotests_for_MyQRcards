from typing import Optional, Dict, List
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CodeMessageModel(StrictBaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(StrictBaseModel):
    list_model: List[CodeMessageModel]


class UserSkillsModel(StrictBaseModel):
    skillID: int
    userID: int
    dateTill: datetime


class UserSkillsListResponseModel(StrictBaseModel):
    results: List[UserSkillsModel]
