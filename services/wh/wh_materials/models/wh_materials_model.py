from typing import Optional, Dict, List
from pydantic import BaseModel, RootModel


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class SuccessAddMaterialsModel(BaseModel):
    result: List[int]


class MaterialModel(BaseModel):
    erpID: Optional[str] = None
    vendorCode: Optional[str] = None
    description: Optional[str] = None
    measurementUnitID: Optional[int] = None
    cost: Optional[float] = None
    costCurrencyID: Optional[int] = None
    purchaseCost: Optional[float] = None
    purchaseCostCurrencyID: Optional[int] = None
    deleted: Optional[str] = None
    name: str
    id: int
