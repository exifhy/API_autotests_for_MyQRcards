from typing import Optional, Dict, List
from pydantic import BaseModel, RootModel


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class SystemRole(BaseModel):
    name: Optional[str] = None
    id: Optional[int] = None


class RolesModel(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    deleted: Optional[str] = None
    systemRoles: Optional[List[SystemRole]] = None


class SuccessGetRolesModel(RootModel):
    root: Dict[str, RolesModel]
