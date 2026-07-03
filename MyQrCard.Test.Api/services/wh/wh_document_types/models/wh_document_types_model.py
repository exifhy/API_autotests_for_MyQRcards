from typing import Optional, Dict, List
from pydantic import BaseModel, ConfigDict, RootModel


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CodeMessageModel(StrictBaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(StrictBaseModel):
    list_model: List[CodeMessageModel]


class CodeNameResult(StrictBaseModel):
    code: str
    name: str


class SuccessGetListDocumentTypesResult(RootModel):
    root: Dict[str, CodeNameResult]
