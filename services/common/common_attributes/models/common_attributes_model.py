from typing import Optional, Dict, List
from pydantic import BaseModel, RootModel


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class SuccessAddAttributeModel(BaseModel):
    values: List[int]


class AttributeTypeResult(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class DomainResult(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    code: Optional[str] = None


class MeasurementUnitResult(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    abbreviation: Optional[str] = None
    designation: Optional[str] = None


class RelevantAttributeResult(BaseModel):
    task: Optional[bool] = None
    asset: Optional[bool] = None
    checkList: Optional[bool] = None
    completedWork: Optional[bool] = None
    contract: Optional[bool] = None
    company: Optional[bool] = None


class AttributeResultList(BaseModel):
    listOfValues: Optional[Dict[str, str]] = None
    name: Optional[str] = None
    type: Optional[AttributeTypeResult] = None
    domain: Optional[DomainResult] = None
    isPublic: Optional[bool] = None
    measurementUnit: Optional[MeasurementUnitResult] = None
    deleted: Optional[str] = None
    relevantFor: Optional[RelevantAttributeResult] = None


class SuccessGetAttributesModel(RootModel):
    root: Optional[Dict[str, AttributeResultList]] = None


class SuccessAvailableValuesForAttributeModel(RootModel):
    root: Optional[Dict[str, str]] = None
