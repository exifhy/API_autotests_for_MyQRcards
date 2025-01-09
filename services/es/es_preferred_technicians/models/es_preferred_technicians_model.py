from pydantic import BaseModel
from typing import List, Optional, Dict


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class UsersPreferredTechniciansModel(BaseModel):
    id: int
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    middleName: Optional[str] = None
    avatarUrl: Optional[str] = None


class AssetsPreferredTechniciansModel(BaseModel):
    parentID: Optional[int] = None
    name: str
    id: int


class SuccessGetPreferredTechniciansModel(BaseModel):
    users: List[UsersPreferredTechniciansModel]
    assets: List[AssetsPreferredTechniciansModel]

