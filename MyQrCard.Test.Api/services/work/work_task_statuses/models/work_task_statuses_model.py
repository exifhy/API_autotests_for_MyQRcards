from datetime import datetime
from typing import Optional, Dict, List
from pydantic import BaseModel, RootModel, ConfigDict


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class SuccessAddWorkTaskStatusesModel(StrictBaseModel):
    status: List[int]


class CodeMessageModel(StrictBaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(StrictBaseModel):
    list_model: List[CodeMessageModel]


class WorkTaskStatusesModel(StrictBaseModel):
    name: str
    color: str
    sortOrder: int


class SuccessGetListWorkTaskStatusesModel(RootModel):
    root: Dict[str, WorkTaskStatusesModel]
