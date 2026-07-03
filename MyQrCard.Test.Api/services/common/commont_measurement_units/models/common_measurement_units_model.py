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


class MeasurementUnitResultModel(StrictBaseModel):
    id: Optional[int] = None
    name: str
    abbreviation: Optional[str] = None
    designation: Optional[str] = None


class SuccessGetMeasurementUnitResultModel(RootModel):
    root: Dict[str, MeasurementUnitResultModel]
