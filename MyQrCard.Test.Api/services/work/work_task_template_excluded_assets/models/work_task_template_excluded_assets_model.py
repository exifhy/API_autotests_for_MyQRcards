from typing import Optional, Dict, List
from pydantic import BaseModel, Field, RootModel, ConfigDict


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CodeMessageModel(StrictBaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(StrictBaseModel):
    list_model: List[CodeMessageModel]


class TaskTemplateExcludedAssetsModel(StrictBaseModel):
    taskTemplateID: str
    assetID: int


class SuccessListTaskTemplateExcludedAssetsModel(StrictBaseModel):
    results: List[TaskTemplateExcludedAssetsModel]
