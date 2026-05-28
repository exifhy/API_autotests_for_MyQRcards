from typing import Optional

from src.models.base import StrictBaseModel


class ReportTypeModel(StrictBaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class PowerBIReportItemModel(StrictBaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    reportID: Optional[str] = None
    workspaceID: Optional[str] = None
    embedUrl: Optional[str] = None
    isCommon: Optional[bool] = None
    reportType: Optional[ReportTypeModel] = None
    reportServiceUrl: Optional[str] = None


class PowerBIReportsListModel(StrictBaseModel):
    items: list[PowerBIReportItemModel]
