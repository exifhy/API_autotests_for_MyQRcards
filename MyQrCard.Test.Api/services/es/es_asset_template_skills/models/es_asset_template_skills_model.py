from typing import Optional, Dict, List
from pydantic import BaseModel


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class SkillsToAssetTemplatesModel(BaseModel):
    assetTemplateID: int
    skillID: int


class SuccessAddSkillsToAssetTemplatesModel(BaseModel):
    result: List[SkillsToAssetTemplatesModel]
