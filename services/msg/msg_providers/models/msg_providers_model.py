from pydantic import BaseModel, RootModel, ConfigDict
from typing import List, Optional, Dict


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CodeMessageModel(StrictBaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(StrictBaseModel):
    list_model: List[CodeMessageModel]


class ProvidersListResultModel(StrictBaseModel):
    id: int
    name: str
    code: str
    descriptionRu: Optional[str] = None


class ProvidersListResponseModel(RootModel):
    root: Dict[str, ProvidersListResultModel]
