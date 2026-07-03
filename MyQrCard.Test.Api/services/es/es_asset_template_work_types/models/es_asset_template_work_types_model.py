from typing import Optional, Dict, List
from pydantic import BaseModel


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class WorkTypesToAssetTemplatesModel(BaseModel):
    assetTemplateID: int
    workTypeID: int


class SuccessAddWorkTypesToAssetTemplatesModel(BaseModel):
    result: List[WorkTypesToAssetTemplatesModel]
