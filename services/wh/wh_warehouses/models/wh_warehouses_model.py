from typing import Optional, Dict, List
from pydantic import BaseModel, RootModel


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class SuccessAddWarehousesModel(BaseModel):
    result: List[int]


class WarehousesModel(BaseModel):
    deleted: Optional[str] = None
    deletedBy: Optional[int] = None
    erpID: Optional[str] = None
    isDefault: Optional[bool] = None
    name: str
    id: int
