from datetime import datetime
from typing import Optional, Dict, List
from pydantic import BaseModel, ConfigDict, RootModel


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


class CostCurrencyModel(StrictBaseModel):
    id: int
    shortName: str
    asciiCode: str


class PurchaseCostCurrencyModel(StrictBaseModel):
    id: int
    shortName: str
    asciiCode: str


class MeasurementUnitModel(StrictBaseModel):
    id: int
    name: str
    abbreviation: str
    designation: str


class MaterialModel(StrictBaseModel):
    erpID: Optional[str] = None
    vendorCode: Optional[str] = None
    description: Optional[str] = None
    measurementUnitID: Optional[int] = None
    measurementUnit: Optional[MeasurementUnitModel] = None
    cost: Optional[float] = None
    costCurrencyID: Optional[int] = None
    costCurrency: Optional[CostCurrencyModel] = None
    purchaseCost: Optional[float] = None
    purchaseCostCurrencyID: Optional[int] = None
    purchaseCostCurrency: Optional[PurchaseCostCurrencyModel] = None
    deleted: Optional[str] = None
    name: str
    id: int
    sortOrder: Optional[int] = None


class SuccessGetListMaterialsV2Model(RootModel):
    root: Dict[str, MaterialModel]


class MaterialAttachmentListResultModel(StrictBaseModel):
    fileName: str
    description: Optional[str] = None
    isUploaded: Optional[bool] = None
    publicUrl: Optional[str] = None
    thumbnailUrl: Optional[str] = None
    isProtected: Optional[bool] = None
    size: int
    created: Optional[datetime] = None


class MaterialAttachmentResultModel(StrictBaseModel):
    fileName: str
    description: Optional[str] = None
    isUploaded: Optional[bool] = None
    publicUrl: Optional[str] = None
    thumbnailUrl: Optional[str] = None
    isProtected: Optional[bool] = None
    size: int
    created: Optional[datetime] = None
    attachmentID: int


class SuccessGetListMaterialAttachmentListResultModel(RootModel):
    root: Dict[str, MaterialAttachmentListResultModel]


class MaterialAttachmentPostResultModel(StrictBaseModel):
    tenantID: int
    materialID: int
    attachmentID: int


class SuccessAddMaterialAttachmentPostResultModel(StrictBaseModel):
    results: List[MaterialAttachmentPostResultModel]


class SuccessGetDownloadMaterialAttachmentModel(StrictBaseModel):
    fileName: str
    url: str
    size: int
    created: datetime


class AttachmentToMaterialModel(StrictBaseModel):
    materialID: int
    attachmentID: int
    md5Hash: str
    fileName: str
    isProtected: bool


class SuccessUploadAttachmentToMaterialModel(StrictBaseModel):
    results: List[AttachmentToMaterialModel]


class IdNameResultModel(StrictBaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class MaterialBarcodeListResultModel(StrictBaseModel):
    id: int
    barcodeType: Optional[IdNameResultModel] = None
    value: Optional[str] = None


class MaterialBarcodesRootModel(RootModel):
    root: Dict[str, List[MaterialBarcodeListResultModel]]


class BarcodesMaterialsModel(StrictBaseModel):
    id: int
    materialID: int


class SuccessAddBarcodesMaterialsModel(StrictBaseModel):
    results: List[BarcodesMaterialsModel]


class CurrencyResult(StrictBaseModel):
    id: Optional[int] = None
    shortName: Optional[str] = None
    asciiCode: Optional[str] = None


class WarehouseResult(StrictBaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    erpID: Optional[str] = None


class IdNameResult(StrictBaseModel):
    id: int
    name: str


class IdNameDeletedResult(StrictBaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    deleted: Optional[datetime] = None


class AssetResult(StrictBaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    deleted: Optional[datetime] = None
    host: Optional[IdNameDeletedResult] = None


class TaskResult(StrictBaseModel):
    id: Optional[int] = None
    number: Optional[str] = None
    asset: Optional[AssetResult] = None


class UserResult(StrictBaseModel):
    id: Optional[int] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    middleName: Optional[str] = None
    avatarUrl: Optional[str] = None
    deleted: Optional[datetime] = None


class MaterialsListResult(StrictBaseModel):
    id: int
    name: str
    erpID: Optional[str] = None
    description: Optional[str] = None
    cost: Optional[float] = None
    currency: Optional[CurrencyResult] = None
    warehouse: Optional[WarehouseResult] = None
    importQuantity: Optional[float] = None
    actualQuantity: Optional[float] = None
    measurementUnit: Optional[IdNameResult] = None
    task: Optional[TaskResult] = None
    taken: Optional[datetime] = None
    takenBy: Optional[UserResult] = None
    sortOrder: Optional[int] = None


class SuccessGetListMaterialsListResultModel(StrictBaseModel):
    results: List[MaterialsListResult]


class MaterialsListRequiredResult(StrictBaseModel):
    id: int
    name: str
    erpID: Optional[str] = None
    description: Optional[str] = None
    cost: float
    currency: Optional[CurrencyResult] = None
    warehouse: Optional[WarehouseResult] = None
    importQuantity: Optional[float] = None
    actualQuantity: Optional[float] = None
    measurementUnit: Optional[IdNameResult] = None
    sortOrder: int


class SuccessGetMaterialsListRequiredResultModel(StrictBaseModel):
    results: List[MaterialsListRequiredResult]
