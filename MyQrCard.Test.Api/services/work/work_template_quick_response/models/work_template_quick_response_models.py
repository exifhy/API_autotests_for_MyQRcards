from datetime import datetime
from typing import Optional, Dict, List
from pydantic import BaseModel, RootModel, ConfigDict


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class TaskTypesModel(StrictBaseModel):
    id: int
    name: str


class TemplateQuickResponseListResult(StrictBaseModel):
    id: int
    name: str
    riposte: str
    taskTypes: Optional[List[TaskTypesModel]] = None
    deleted: Optional[datetime] = None


class SuccessTemplateQuickResponseModel(RootModel):
    root: Dict[str, TemplateQuickResponseListResult]


class SuccessAddTemplateQuickResponseModel(StrictBaseModel):
    results: List[int]

