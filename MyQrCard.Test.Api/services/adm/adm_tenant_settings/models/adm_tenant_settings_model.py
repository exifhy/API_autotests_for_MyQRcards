from pydantic import BaseModel, ConfigDict, RootModel
from typing import List, Optional, Dict
from datetime import datetime


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CodeMessageModel(StrictBaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(StrictBaseModel):
    results: List[CodeMessageModel]


class CurrencyResult(StrictBaseModel):
    id: Optional[int] = None
    shortName: Optional[str] = None
    asciiCode: Optional[str] = None


class TenantSettingsGetResultModel(StrictBaseModel):
    geoDataRetentionMonths: Optional[int] = None
    supportEmail: Optional[str] = None
    supportPhone: Optional[str] = None
    storageApiUrl: Optional[str] = None
    storageUrl: Optional[str] = None
    storageProviderID: Optional[int] = None
    defaultTimezoneID: Optional[int] = None
    defaultMailBoxID: Optional[int] = None
    defaultCurrency: Optional[CurrencyResult] = None
    realm: Optional[str] = None
