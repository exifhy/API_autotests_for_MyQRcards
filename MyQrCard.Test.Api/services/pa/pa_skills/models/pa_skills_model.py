from typing import Optional, Dict, List
from pydantic import BaseModel, Field, RootModel, ConfigDict
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


class AssSkillsModel(StrictBaseModel):
    skillID: int


class SuccessAddSkillsModel(StrictBaseModel):
    skills: List[AssSkillsModel]


class Counters(StrictBaseModel):
    tasks: Optional[int] = None
    assets: Optional[int] = None
    users: Optional[int] = None


class ListResult(StrictBaseModel):
    counters: Optional[Counters] = None
    isOptional: Optional[bool] = None
    name: Optional[str] = None
    id: Optional[int] = None


class SuccessGetSkillsListResultModel(RootModel):
    root: Dict[str, ListResult]


class SuccessGetSkillByIdResultModel(StrictBaseModel):
    description: Optional[str] = None
    deleted: Optional[datetime] = None
    isOptional: Optional[bool] = None
    name: str
    id: int
