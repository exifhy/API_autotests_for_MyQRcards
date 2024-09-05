from typing import Optional, Dict, List
from pydantic import BaseModel
from datetime import datetime


class SuccessUserModel(BaseModel):
    tenantID: Optional[int] = None
    tenantMemberID: Optional[int] = None
    userID: Optional[int] = None
    isPasswordDefined: Optional[bool] = None
    isNewAccount: Optional[bool] = None
    id: Optional[int] = None
    isEmailVerified: Optional[bool] = None
    isMobilePhoneVerified: Optional[bool] = None
    verificationRequestValidTill: Optional[datetime] = None


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]