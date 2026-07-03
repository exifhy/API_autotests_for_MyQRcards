from pydantic import BaseModel, ConfigDict, RootModel
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


class UserOrderByModel(StrictBaseModel):
    name: str
    code: str


class UserOrderByListResponseModel(RootModel):
    root: Dict[str, UserOrderByModel]
