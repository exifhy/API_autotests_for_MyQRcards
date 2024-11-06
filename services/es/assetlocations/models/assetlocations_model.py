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


class LocationModel(BaseModel):
    dateFrom: Optional[datetime] = None
    dateTill: Optional[datetime] = None
    timezoneUtcOffsetMinutes: Optional[int] = None
    timezoneID: Optional[int] = None
    countryID: Optional[int] = None
    countryTwoSymbolCode: Optional[str] = None
    address: Optional[str] = None
    coordinate: Optional[str] = None
    id: Optional[int] = None


class GetAssetLocationModel(BaseModel):
    assetID: int
    location: Optional[LocationModel]


class SuccessGetAssetLocationModel(RootModel):
    root: Optional[Dict[str, GetAssetLocationModel]] = None
