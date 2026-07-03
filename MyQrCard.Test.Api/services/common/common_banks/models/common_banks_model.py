from typing import Optional, Dict, List
from pydantic import BaseModel, RootModel


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class BanksInfoModel(BaseModel):
    id: int
    name: str
    bic: Optional[str] = None
    correspondingAccount: Optional[str] = None
    swift: Optional[str] = None
    phone: Optional[str] = None
    eMail: Optional[str] = None
    address: Optional[str] = None
    isActive: Optional[bool] = None


class SuccessGetListBanksModel(RootModel):
    root: Dict[str, BanksInfoModel]