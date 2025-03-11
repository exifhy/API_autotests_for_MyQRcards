from enum import Enum
import pytest
import random
import string


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

    params_auth_accounts = [
        pytest.param("5", "10", id="offset=5, fetch=10"),
        pytest.param("0", "50", id="offset=0, fetch=50"),
        pytest.param("20", "20", id="offset=20, fetch=20")
    ]

    params_auth_accounts_negative = [
        pytest.param("offset", "-5", id="offset=-5"),
        pytest.param("fetch", "abc", id="fetch=abc"),
        pytest.param("fetch", "1000000000", id="fetch=1000000000")
    ]

    params_auth_accounts_negative_range = [
        pytest.param("Range", "items=10-0", id="Range=items=10-0"),
        pytest.param("Range", "items=0-abc", id="Range=items=0-abc")
    ]

    params_auth_change_passwords = [
        pytest.param({
            "Password": "02022014",
            "CodeHash": "6dae72cdce875817968eacf0093ce9548f60243c3e46f1d632352d1a22a8893e"
        }, id="Change password with codeHash"),
        pytest.param({
            "password": "string",
            "currentPassword": "string"
        }, id="Change password with currentPassword"),
        pytest.param({
            "code": "code",
            "MobilePhone": "+7number",
            "Password" : "password"
        }, id="Change password with code, mobilePhone")
    ]

    params_auth_verification_codes = [
        pytest.param({}, id=""),
    ]

    params_authn_set_passwords = [
        pytest.param({
            "Password": "02022014",
            "CodeHash": "6dae72cdce875817968eacf0093ce9548f60243c3e46f1d632352d1a22a8893e"
        }, id="Change password with codeHash")
    ]

    params_post_task_number = [
        pytest.param(''.join(random.choice(string.ascii_letters) for _ in range(32))
                     , 201, 32, id="Task number length 32 (string)."),
        pytest.param(''.join(random.choice(string.ascii_letters) for _ in range(31))
                     , 201, 31, id="Task number length 31 (string)."),
        pytest.param(''.join(random.choice(string.ascii_letters) for _ in range(33))
                     , 409, 0, id="Task number length 33 (string)."),
        pytest.param(random.randint(10000000000000000000000000000000, 99999999999999999999999999999999),
                     201, 32, id="Task number length 32 (integer)."),
    ]

    params_put_task_number = [
        pytest.param(''.join(random.choice(string.ascii_letters) for _ in range(32))
                     , 202, 32, id="Task number length 32 (string)."),
        pytest.param(''.join(random.choice(string.ascii_letters) for _ in range(31))
                     , 202, 31, id="Task number length 31 (string)."),
        pytest.param(''.join(random.choice(string.ascii_letters) for _ in range(33))
                     , 409, 0, id="Task number length 33 (string)."),
        pytest.param(random.randint(10000000000000000000000000000000, 99999999999999999999999999999999),
                     202, 32, id="Task number length 32 (integer)."),
    ]

    params_patch_task_number = [
        pytest.param(''.join(random.choice(string.ascii_letters) for _ in range(32))
                     , 202, 32, id="Task number length 32 (string)."),
        pytest.param(''.join(random.choice(string.ascii_letters) for _ in range(31))
                     , 202, 31, id="Task number length 31 (string)."),
        pytest.param(''.join(random.choice(string.ascii_letters) for _ in range(33))
                     , 409, 0, id="Task number length 33 (string)."),
        pytest.param(random.randint(10000000000000000000000000000000, 99999999999999999999999999999999),
                     409, 32, id="Task number length 32 (integer)."),
    ]

    params_export_task_number = [
        pytest.param(''.join(random.choice(string.ascii_letters) for _ in range(32))
                     , 201, 32, id="Task number length 32 (string)."),
        pytest.param(''.join(random.choice(string.ascii_letters) for _ in range(31))
                     , 201, 31, id="Task number length 31 (string)."),
        pytest.param(random.randint(10000000000000000000000000000000, 99999999999999999999999999999999),
                     201, 32, id="Task number length 32 (integer)."),
    ]
