from typing import Optional, Dict, List
from pydantic import BaseModel, RootModel
from datetime import datetime


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class InventoriesModel(BaseModel):
    id: int
    dateFrom: datetime
    dateTill: datetime


class SuccessAddInventoriesModel(BaseModel):
    result: List[InventoriesModel]
