from typing import Optional, List, Dict
from pydantic import BaseModel
from datetime import datetime


class AccountsVerificationResult(BaseModel):
    id: Optional[int] = None
    isEmailVerified: Optional[bool] = None
    isPhoneVerified: Optional[bool] = None
    verificationRequestValidTill: Optional[datetime] = None
    isPasswordDefined: Optional[bool] = None
    isNewAccount: Optional[bool] = None
    verificationCodeRepeatTimeout: Optional[int] = None


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]
