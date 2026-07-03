from pydantic import BaseModel, RootModel
from typing import List, Optional, Dict


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class CompanyModel(BaseModel):
    name: str
    id: int


class OrgUnitsModel(BaseModel):
    name: str
    hasChildren: bool
    company: Optional[CompanyModel] = None


class SuccessGetListOrgUnitsModel(RootModel):
    root: Dict[str, OrgUnitsModel]
