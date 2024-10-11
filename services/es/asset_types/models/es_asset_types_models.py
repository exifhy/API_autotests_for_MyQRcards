from pydantic import BaseModel, RootModel
from typing import List, Optional, Dict


class AssetTypeListResult(BaseModel):
    name: Optional[str] = None
    isHostable: Optional[bool] = None
    isDefault: Optional[bool] = None


class SuccessGetAssetTypeModel(RootModel):
    root: Dict[str, AssetTypeListResult]


class SuccessAddAssetTypesModel(BaseModel):
    id: List[int]


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]
