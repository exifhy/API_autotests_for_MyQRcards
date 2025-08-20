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


class SuccessAddAttributeModel(StrictBaseModel):
    values: List[int]


class AttributeTypeResult(StrictBaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class DomainResult(StrictBaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    code: Optional[str] = None


class MeasurementUnitResult(StrictBaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    abbreviation: Optional[str] = None
    designation: Optional[str] = None


class RelevantAttributeResult(StrictBaseModel):
    task: Optional[bool] = None
    asset: Optional[bool] = None
    checkList: Optional[bool] = None
    completedWork: Optional[bool] = None
    contract: Optional[bool] = None
    company: Optional[bool] = None
    customer: Optional[bool] = None
    technician: Optional[bool] = None


class AttributeResultList(StrictBaseModel):
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
