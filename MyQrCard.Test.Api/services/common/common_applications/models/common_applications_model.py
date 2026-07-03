from typing import Optional, Dict, List
from pydantic import BaseModel, RootModel, ConfigDict


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ApplicationResult(StrictBaseModel):
    code: str
    nameRu: str


class SuccessGetApplicationResultModel(RootModel):
    root: Dict[str, ApplicationResult]


class CodeMessageModel(StrictBaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(StrictBaseModel):
    list_model: List[CodeMessageModel]


class SuccessAddAttributeModel(StrictBaseModel):
    values: List[int]
