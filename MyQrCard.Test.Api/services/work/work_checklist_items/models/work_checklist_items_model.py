from typing import Optional, Dict, List
from pydantic import BaseModel


class AddChecklistItemsModel(BaseModel):
    tenantID: Optional[int] = None
    checkListID: int
    checkListItemID: int
    id: Optional[int] = None


class SuccessAddChecklistItemsModel(BaseModel):
    result: List[AddChecklistItemsModel]


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]
