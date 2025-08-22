from pydantic import BaseModel, ConfigDict, constr
from typing import List, Optional, Dict


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CodeMessageModel(StrictBaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(StrictBaseModel):
    list_model: List[CodeMessageModel]


class LayoutFieldDto(StrictBaseModel):
    id: Optional[int] = None
    index: Optional[int] = None
    label: constr(min_length=1, max_length=256)
    type: Optional[int] = None
    code: constr(min_length=1)
    color: Optional[str] = None
    img: Optional[str] = None


class LayoutBlockDto(StrictBaseModel):
    id: Optional[int] = None
    index: Optional[int] = None
    name: Optional[str] = None
    fields: List[LayoutFieldDto] = []


class LayoutColumnDto(StrictBaseModel):
    id: Optional[int] = None
    index: int
    blocks: List[LayoutBlockDto] = []


class LayoutTemplateDtoModel(StrictBaseModel):
    id: Optional[int] = None
    isDefault: Optional[bool] = None
    name: Optional[str] = None
    columns: List[LayoutColumnDto] = []
    taskTypes: Optional[List[int]] = None


class LayoutTemplateDtoListModel(StrictBaseModel):
    result: List[LayoutTemplateDtoModel]


class LayoutTaskTypeDtoModel(StrictBaseModel):
    id: int
    name: str


class ListLayoutTaskTypeDtoModel(StrictBaseModel):
    results: List[LayoutTaskTypeDtoModel]


class LayoutTaskTypeDtoListModel(StrictBaseModel):
    result: List[LayoutTaskTypeDtoModel]


class ComponentDtoModel(StrictBaseModel):
    id: int
    code: str
    description: Optional[str] = None
    isRequired: Optional[bool] = None
    isInUse: Optional[bool] = None


class ComponentDtoListModel(StrictBaseModel):
    result: List[ComponentDtoModel]


class AttributeDtoModel(StrictBaseModel):
    id: int
    name: str
    isInUse: Optional[bool] = None


class AttributeDtoListModel(StrictBaseModel):
    result: List[AttributeDtoModel]
