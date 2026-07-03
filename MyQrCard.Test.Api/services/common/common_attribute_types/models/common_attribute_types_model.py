from typing import Dict, List, Optional
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


class AttributeTypesListResultModel(StrictBaseModel):
    code: str
    name: str


class SuccessGetAttributeTypesListResultModel(RootModel):
    root: Dict[str, AttributeTypesListResultModel]


class AttributesDomainResultModel(StrictBaseModel):
    id: int
    name: str
    code: str


class AttributeTypesExtListResultModel(StrictBaseModel):
    code: str
    name: str
    id: int
    domain: Optional[AttributesDomainResultModel] = None


class SuccessGetAttributeTypesExtListResultV2Model(StrictBaseModel):
    results: List[AttributeTypesExtListResultModel]
