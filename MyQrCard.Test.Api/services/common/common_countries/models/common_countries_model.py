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


class CountriesListResultModel(StrictBaseModel):
    name: str
    twoSymbolCode: str
    threeSymbolCode: str


class SuccessGetCountriesListResultModel(RootModel):
    root: Dict[str, CountriesListResultModel]
