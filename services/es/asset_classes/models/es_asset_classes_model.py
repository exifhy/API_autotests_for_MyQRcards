from pydantic import BaseModel, RootModel
from typing import List, Optional, Dict
from datetime import datetime


class AssetClassesResult(BaseModel):
    name: Optional[str] = None
    id: Optional[int] = None
    isDefault: Optional[bool] = None
    deleted: Optional[datetime] = None


class SuccessGetAssetClassesModel(RootModel):
    root: Dict[str, AssetClassesResult]


class AddAssetClassesModel(BaseModel):
    id: int


class SuccessAddAssetClassesModel(BaseModel):
    list: List[AddAssetClassesModel]


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]
