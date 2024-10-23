from pydantic import BaseModel, RootModel
from typing import List, Optional, Dict
from datetime import datetime


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class SuccessAddServiceContractModel(BaseModel):
    contract: List[int]


class AddListObjectsToContractModel(BaseModel):
    tenantID: Optional[int] = None
    contractID: Optional[int] = None
    assetID: Optional[int] = None
    isNew: Optional[bool] = None


class SuccessAddListObjectsToContractModel(BaseModel):
    objects: List[AddListObjectsToContractModel]


class SuccessGetContractResultModel(BaseModel):
    contractID: Optional[int] = None
    companyID: Optional[int] = None
    companyName: Optional[str] = None
    name: Optional[str] = None
    number: Optional[str] = None
    description: Optional[str] = None
    conditions: Optional[str] = None
    dateFrom: Optional[datetime] = None
    dateTill: Optional[datetime] = None
    remindExpirationDate: Optional[bool] = None
    reminderDate: Optional[datetime] = None
    isDeleted: Optional[bool] = None


class ContractListResult(BaseModel):
    contractID: Optional[int] = None
    companyID: Optional[int] = None
    companyName: Optional[str] = None
    name: Optional[str] = None
    number: Optional[str] = None
    description: Optional[str] = None
    conditions: Optional[str] = None
    dateFrom: Optional[datetime] = None
    dateTill: Optional[datetime] = None


class SuccessGetMassContractDictModel(RootModel):
    root: Dict[str, ContractListResult]


class ListContractObjectsModel(BaseModel):
    assetID: Optional[int] = None
    contractID: Optional[int] = None
    tenantID: Optional[int] = None


class SuccessGetListContractObjectsModel(RootModel):
    root: Dict[str, ListContractObjectsModel]
