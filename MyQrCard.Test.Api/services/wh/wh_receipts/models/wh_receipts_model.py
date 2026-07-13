from datetime import datetime
from typing import Optional, Dict, List
from pydantic import BaseModel, RootModel, ConfigDict


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CodeMessageModel(StrictBaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(StrictBaseModel):
    list_model: List[CodeMessageModel]


class IdCodeNameResult(BaseModel):
    id: int
    code: Optional[str] = None
    name: Optional[str] = None


class SuccessAddReceiptsModel(StrictBaseModel):
    result: List[int]


class SuccessRestoreReceiptsModel(StrictBaseModel):
    result: List[int]


class IdNameResult(StrictBaseModel):
    id: int
    name: Optional[str] = None


class ReceiptResultModel(StrictBaseModel):
    id: int
    name: Optional[str] = None
    warehouseID: int
    warehouseName: Optional[str] = None
    documentStatus: IdCodeNameResult
    documentStatusName: Optional[str] = None
    documentDate: Optional[datetime] = None
    number: Optional[str] = None
    erpID: Optional[str] = None
    description: Optional[str] = None
    deleted: Optional[datetime] = None
    operationType: IdNameResult
    created: datetime
    modified: Optional[datetime] = None
    posted: Optional[datetime] = None
    relatedTaskID: Optional[int] = None
    taskNumber: Optional[str] = None
    responsiblePerson: Optional[IdNameResult] = None


class SuccessGetListReceiptResultModel(RootModel):
    root: Dict[str, ReceiptResultModel]


class MaterialResult(StrictBaseModel):
    id: int
    name: Optional[str] = None
    erpID: Optional[str] = None
    vendorCode: Optional[str] = None
    description: Optional[str] = None
    measurementUnitID: Optional[int] = None
    cost: Optional[float] = None
    costCurrencyID: Optional[int] = None
    purchaseCost: Optional[float] = None
    purchaseCostCurrencyID: Optional[int] = None
    deleted: Optional[datetime] = None


class ReceiptItemsListResultModel(StrictBaseModel):
    receiptID: int
    material: MaterialResult
    measurementUnit: IdNameResult
    quantity: float


class SuccessGetListReceiptItemsModel(StrictBaseModel):
    results: List[ReceiptItemsListResultModel]
