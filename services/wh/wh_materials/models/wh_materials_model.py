from typing import Optional, Dict, List
from pydantic import BaseModel, ConfigDict


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CodeMessageModel(StrictBaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(StrictBaseModel):
    list_model: List[CodeMessageModel]


class SuccessAddMaterialsModel(StrictBaseModel):
    result: List[int]


class MaterialModel(StrictBaseModel):
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
