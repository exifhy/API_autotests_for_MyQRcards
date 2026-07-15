from src.models.base import StrictBaseModel


class ManagerDailyLimitModel(StrictBaseModel):
    dailyLimit: int
    usedToday: int
