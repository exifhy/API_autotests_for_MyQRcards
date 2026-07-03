from typing import Optional, Dict, List
from pydantic import BaseModel


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class AddTagsToAssetModel(BaseModel):
    assetID: int
    tag: str


class SuccessAddTagsToAssetModel(BaseModel):
    result: List[AddTagsToAssetModel]

