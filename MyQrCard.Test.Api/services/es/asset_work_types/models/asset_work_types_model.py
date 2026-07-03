from typing import Optional, Dict, List
from pydantic import BaseModel


class AssetWorkTypeProjection(BaseModel):
    tenantID: Optional[int] = None
    assetID: Optional[int] = None
    workTypeID: Optional[int] = None
    path: Optional[str] = None


class SuccessAssetWorkTypeModel(BaseModel):
    asset: List[AssetWorkTypeProjection]


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]