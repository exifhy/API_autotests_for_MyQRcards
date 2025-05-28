from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CodeMessageModel(StrictBaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(StrictBaseModel):
    results: List[CodeMessageModel]


class UserAssetListQueriesPostResultModel(StrictBaseModel):
    assetListQueryID: int
    userID: int


class UserAssetListQueriesListResponseModel(StrictBaseModel):
    results: List[UserAssetListQueriesPostResultModel]
