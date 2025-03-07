from typing import List
from pydantic import BaseModel


class AddWorkTaskSkillsModel(BaseModel):
    taskID: int
    skillID: int


class SuccessAddWorkTaskSkillsModel(BaseModel):
    results: List[AddWorkTaskSkillsModel]
