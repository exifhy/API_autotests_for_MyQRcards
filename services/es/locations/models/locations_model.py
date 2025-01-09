from pydantic import BaseModel, RootModel
from typing import List, Optional, Dict


class SuccessAddLocationModel(BaseModel):
    location: List[int]


class SuccessUpdateLocationModel(BaseModel):
    location: List[int]


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class TimeZoneResult(BaseModel):
    utcOffsetMinutes: Optional[int] = None
    name: Optional[str] = None
    id: Optional[int] = None


class CountryResult(BaseModel):
    twoSymbolCode: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class LocationResultModel(BaseModel):
    area: Optional[List[str]] = None
    address: Optional[str] = None
    coordinate: Optional[str] = None
    description: Optional[str] = None
    deleted: Optional[str] = None
    timeZone: Optional[TimeZoneResult] = None
    country: Optional[CountryResult] = None
    id: Optional[int] = None


class SuccessGetListLocationsModel(RootModel):
    root: Dict[str, LocationResultModel]

