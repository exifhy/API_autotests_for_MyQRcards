from typing import Optional, Dict, List
from pydantic import BaseModel, ConfigDict


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CodeMessageModel(StrictBaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(StrictBaseModel):
    list_model: List[CodeMessageModel]


class ResultModel(StrictBaseModel):
    code: Optional[str] = None
    description: Optional[str] = None


class SuccessTasksResultModel(StrictBaseModel):
    list: List[ResultModel]

