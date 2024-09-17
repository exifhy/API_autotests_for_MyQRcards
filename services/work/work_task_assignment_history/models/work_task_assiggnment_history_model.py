from typing import Optional, List, Dict
from pydantic import BaseModel


class Assignment(BaseModel):
    userID: Optional[int] = None
    dateTimeFrom: Optional[str] = None
    dateTimeTill: Optional[str] = None
    error: Optional[str] = None


class AddResult(BaseModel):
    taskID: Optional[int] = None
    taskNumber: Optional[str] = None
    sortOrder: Optional[int] = None
    assignments: Optional[List[Assignment]] = None


class SuccessAddTaskAssignmentHistoryModel(BaseModel):
    history: List[AddResult]


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]
