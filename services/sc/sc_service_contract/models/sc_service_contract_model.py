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


class IdNameDeletedResult(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    deleted: Optional[datetime] = None


class AttributeTypeResult(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    code: Optional[str] = None


class MeasurementUnitResult(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    abbreviation: Optional[str] = None
    designation: Optional[str] = None


class DomainResult(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    code: Optional[str] = None


class GetContractAttributeResultModel(BaseModel):
    attribute: Optional[IdNameDeletedResult] = None
    values: Optional[List[Optional[str]]] = None
    isPublic: Optional[bool] = None
    attributeType: Optional[AttributeTypeResult] = None
    measurementUnit: Optional[MeasurementUnitResult] = None
    listOfValues: Optional[Dict[str, Optional[str]]] = None
    domain: Optional[DomainResult] = None


class SuccessGetContractAttributeResultModel(BaseModel):
    attributes: Optional[List[GetContractAttributeResultModel]] = None


class GetListServiceContractObjectsModel(BaseModel):
    tenantID: Optional[int] = None
    contractID: Optional[int] = None
    assetID: Optional[int] = None


class SuccessGetListServiceContractObjectsModel(RootModel):
    root: Dict[str, GetListServiceContractObjectsModel]


class SuccessUploadResultModel(BaseModel):
    attachmentID: Optional[int] = None
    md5Hash: Optional[str] = None
    fileName: Optional[str] = None
    isProtected: Optional[bool] = None
    contractID: Optional[int] = None


class AttachmentListResult(BaseModel):
    fileName: Optional[str] = None
    description: Optional[str] = None
    isUploaded: Optional[bool] = None
    publicUrl: Optional[str] = None
    thumbnailUrl: Optional[str] = None
    isProtected: Optional[bool] = None
    size: Optional[int] = None
    created: Optional[str] = None
    attachmentID: Optional[int] = None


class SuccessGetAttachmentListResultModel(RootModel):
    root: Dict[str, AttachmentListResult]


class BindAttachmentToContractModel(BaseModel):
    tenantID: Optional[int] = None
    contractID: Optional[int] = None
    attachmentID: Optional[int] = None


class SuccessBindAttachmentToContractModel(BaseModel):
    attachments: Optional[List[BindAttachmentToContractModel]] = None


class AddContactsToContractModel(BaseModel):
    tenantID: Optional[int] = None
    contractID: Optional[int] = None
    contactID: Optional[int] = None
    isNew: Optional[bool] = None


class SuccessAddContactsToContractModel(BaseModel):
    objects: Optional[List[AddContactsToContractModel]] = None


class ListContactsResponsibleToContract(BaseModel):
    contractID: Optional[int] = None
    contactID: Optional[int] = None


class SuccessListContactsResponsibleToContract(RootModel):
    root: Optional[Dict[str, ListContactsResponsibleToContract]] = None
