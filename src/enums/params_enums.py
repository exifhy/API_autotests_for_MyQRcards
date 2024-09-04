from enum import Enum
import pytest


class Params(Enum):

    params_assets_list = [
        pytest.param(
            {
                "isDeleted": "false",
                "includePath": "false",
                "includeTaskActuality": "false"
            }, id="isDeleted=false, includePath=false, includeTaskActuality=false")
    ]

    params_work_types = [
        pytest.param({"relatedToAnyTaskType": "true"}, id="relatedToAnyTaskType=true")
    ]

    params_export_assets = [
        pytest.param({"include": "ErpID"}, id="include: ErpID"),
        pytest.param({"include": "LocationAddress"}, id="include: LocationAddress"),
        pytest.param({"include": "WorkTypeName"}, id="include: WorkTypeName"),
        pytest.param({"include": "LocationLongitude"}, id="include: LocationLongitude"),
        pytest.param({"include": "AssetClassName"}, id="include: AssetClassName"),
        pytest.param({"include": "AssetContactFullName"}, id="include: AssetContactFullName"),
        pytest.param({"include": "AssetContactDescription"}, id="include: AssetContactDescription"),
        pytest.param({"include": "CompanyName"}, id="include: CompanyName"),
        pytest.param({"include": "IsMobileAsset"}, id="include: IsMobileAsset"),
        pytest.param({"include": "Name"}, id="include: Name"),
        pytest.param({"include": "Notes"}, id="include: Notes"),
        pytest.param({"include": "LocationDescription"}, id="include: LocationDescription"),
        pytest.param({"include": "ResponsiblePersonFullName"}, id="include: ResponsiblePersonFullName"),
        pytest.param({"include": "ParentAssetName"}, id="include: ParentAssetName"),
        pytest.param({"include": "SerialNumber"}, id="include: SerialNumber"),
        pytest.param({"include": "LocationCountryNameRu"}, id="include: LocationCountryNameRu"),
        pytest.param({"include": "AssetContactPhone"}, id="include: AssetContactPhone"),
        pytest.param({"include": "AssetTypeName"}, id="include: AssetTypeName"),
        pytest.param({"include": "DistrictName"}, id="include: DistrictName"),
        pytest.param({"include": "LocationTimezoneNameRu"}, id="include: LocationTimezoneNameRu"),
        pytest.param({"include": "LocationLatitude"}, id="include: LocationLatitude"),
        pytest.param({"include": "AssetContactEmail"}, id="include: AssetContactEmail"),
        pytest.param({"include": "LocationTimezoneNameRu"}, id="include: LocationTimezoneNameRu"),
        pytest.param({"isDeleted": "false"}, id="isDeleted: false"),
        pytest.param({"isDeleted": "true"}, id="isDeleted: true"),
        pytest.param({"isPublished": "true"}, id="isPublished: true"),
        pytest.param({"isPublished": "false"}, id="isPublished: false"),
        pytest.param({"includePath": "false"}, id="includePath: false"),
        pytest.param({"includePath": "true"}, id="includePath: true"),
        pytest.param({"includeTaskActuality": "true"}, id="includeTaskActuality: true"),
        pytest.param({"includeTaskActuality": "false"}, id="includeTaskActuality: false"),
        pytest.param({"warrantyTill": "9999-12-31T23:59:59"}, id="warrantyTill: 9999-12-31T23:59:59")
    ]
