from typing import Optional, Dict, List
from pydantic import BaseModel, Field, RootModel
from datetime import datetime


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class AssSkillsModel(BaseModel):
    skillID: int


class SuccessAddSkillsModel(BaseModel):
    skills: List[AssSkillsModel]


class Counters(BaseModel):
    tasks: Optional[int] = None
    assets: Optional[int] = None
    users: Optional[int] = None


class ListResult(BaseModel):
    counters: Optional[Counters] = None
    isOptional: Optional[bool] = None
    name: Optional[str] = None
    id: Optional[int] = None


class SuccessGetSkillsListResultModel(RootModel):
    root: Dict[str, ListResult]


class SuccessGetSkillByIdResultModel(BaseModel):
    description: Optional[str] = None
    deleted: Optional[datetime] = None
    isOptional: Optional[bool] = None
    name: str
    id: int
