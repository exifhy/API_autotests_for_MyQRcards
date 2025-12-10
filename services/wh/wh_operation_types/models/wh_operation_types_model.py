from datetime import datetime
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


class IdCodeNameResult(StrictBaseModel):
    id: int
    code: Optional[str] = None
    name: Optional[str] = None


class IdResultModel(StrictBaseModel):
    id: int


class SuccessGetOperationTypeResult(StrictBaseModel):
    id: int
    name: Optional[str] = None
    erpID: Optional[str] = None
    deleted: Optional[datetime] = None
    documentType: Optional[IdCodeNameResult] = None


class SuccessGetListOperationTypeResult(RootModel):
    root: Dict[str, SuccessGetOperationTypeResult]


class SuccessOperationTypeAddResultModel(StrictBaseModel):
    results: List[IdResultModel]
