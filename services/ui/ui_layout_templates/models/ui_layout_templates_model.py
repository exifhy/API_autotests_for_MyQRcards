from pydantic import BaseModel, ConfigDict, constr
from typing import List, Optional, Dict, Literal


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
    name: constr(min_length=1)
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
