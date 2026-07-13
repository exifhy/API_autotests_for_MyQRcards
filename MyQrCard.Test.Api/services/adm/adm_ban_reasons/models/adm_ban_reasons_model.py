from typing import Optional, Dict, List
from pydantic import BaseModel, RootModel, ConfigDict


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CodeMessageModel(StrictBaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(StrictBaseModel):
    list_model: List[CodeMessageModel]


class BanReasonsListResultModel(StrictBaseModel):
    code: str
    name: str
    description: Optional[str] = None


class SuccessGetBanReasonsListResultModel(RootModel):
    root: Dict[str, BanReasonsListResultModel]
