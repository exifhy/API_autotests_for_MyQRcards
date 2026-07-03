from typing import Optional
from pydantic import BaseModel


class SuccessAccountJwtResultBase(BaseModel):
    jwtValidTill: Optional[str] = None
    accountUserTypeID: Optional[int] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
