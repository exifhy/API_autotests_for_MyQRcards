from typing import Optional, List, Dict
from pydantic import BaseModel


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class TaskStagingHistoryModel(BaseModel):
    taskID: int
    taskStageID: int
    error: Optional[str] = None


class SuccessTaskStagingHistoryModel(BaseModel):
    history: List[TaskStagingHistoryModel]
