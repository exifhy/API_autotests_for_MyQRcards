from pydantic import BaseModel, RootModel
from typing import List, Optional, Dict


class SuccessAddContactModel(BaseModel):
    contact: List[int]


class ContactModel(BaseModel):
    id: Optional[int] = None
    fullName: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    position: Optional[str] = None
    description: Optional[str] = None
    deleted: Optional[str] = None
    isUsed: Optional[bool] = None


class SuccessGetListContactsModel(RootModel):
    root: Dict[str, ContactModel]
