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


class LocationDataModel(BaseModel):
    dateFrom: Optional[datetime] = None
    dateTill: Optional[datetime] = None
    timezoneUtcOffsetMinutes: Optional[int] = None
    timezoneID: Optional[int] = None
    countryID: Optional[int] = None
    countryTwoSymbolCode: Optional[str] = None
    address: str
    coordinate: str
    id: int


class ListCompanyLocationsModel(BaseModel):
    companyID: int
    location: LocationDataModel


class SuccessGetListCompanyLocationsModel(RootModel):
    root: Dict[str, ListCompanyLocationsModel]

