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


class TimeZonesListResultsModel(StrictBaseModel):
    name: str
    utcTimeOffset: str


class SuccessGetTimeZonesListResultsModel(RootModel):
    root: Dict[str, TimeZonesListResultsModel]


class TimeZonesInfoListResultsModel(StrictBaseModel):
    name: str
    utcTimeOffsetMinutes: int


class SuccessGetTimeZonesInfoListResultsModel(StrictBaseModel):
    results: List[TimeZonesInfoListResultsModel]
