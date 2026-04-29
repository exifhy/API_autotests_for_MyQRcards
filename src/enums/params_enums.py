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
            "Password": "password"
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
        pytest.param(''.join(random.choice(string.ascii_letters) for _ in range(32)),
                     201, 32, id="Task number length 32 (string)."),
        pytest.param(''.join(random.choice(string.ascii_letters) for _ in range(31)),
                     201, 31, id="Task number length 31 (string)."),
        pytest.param(''.join(random.choice(string.ascii_letters) for _ in range(33)),
                     409, 0, id="Task number length 33 (string)."),
        pytest.param(random.randint(10000000000000000000000000000000, 99999999999999999999999999999999),
                     201, 32, id="Task number length 32 (integer)."),
    ]

    params_put_task_number = [
        pytest.param(''.join(random.choice(string.ascii_letters) for _ in range(32)),
                     202, 32, id="Task number length 32 (string)."),
        pytest.param(''.join(random.choice(string.ascii_letters) for _ in range(31)),
                     202, 31, id="Task number length 31 (string)."),
        pytest.param(''.join(random.choice(string.ascii_letters) for _ in range(33)),
                     409, 0, id="Task number length 33 (string)."),
        pytest.param(random.randint(10000000000000000000000000000000, 99999999999999999999999999999999),
                     202, 32, id="Task number length 32 (integer)."),
    ]

    params_patch_task_number = [
        pytest.param(''.join(random.choice(string.ascii_letters) for _ in range(32)),
                     202, 32, id="Task number length 32 (string)."),
        pytest.param(''.join(random.choice(string.ascii_letters) for _ in range(31)),
                     202, 31, id="Task number length 31 (string)."),
        pytest.param(''.join(random.choice(string.ascii_letters) for _ in range(33)),
                     409, 0, id="Task number length 33 (string)."),
        pytest.param(random.randint(10000000000000000000000000000000, 99999999999999999999999999999999),
                     409, 32, id="Task number length 32 (integer)."),
    ]

    params_export_task_number = [
        pytest.param(''.join(random.choice(string.ascii_letters) for _ in range(32)),
                     201, 32, id="Task number length 32 (string)."),
        pytest.param(''.join(random.choice(string.ascii_letters) for _ in range(31)),
                     201, 31, id="Task number length 31 (string)."),
        pytest.param(random.randint(10000000000000000000000000000000, 99999999999999999999999999999999),
                     201, 32, id="Task number length 32 (integer)."),
    ]

    params_negative_warehouse_body = [
        pytest.param({"ErpID": "ErpID 67"}, "InvalidData", "The Name field is required.",
                     "Successful processing of a request without the name field",
                     id="Request body without <name> field."),
        pytest.param({"Name": "", "ErpID": "ErpID 67"}, "InvalidData", "The Name field is required.",
                     "Successful processing of a request with empty <name> field",
                     id="Request body with empty <name> field."),
        pytest.param({}, "InvalidData", "The Name field is required.",
                     "Successful processing of a request with empty dict",
                     id="Request body with {}."),
        pytest.param({"Name": "Склад 67", "ErpID": f"{"A"*65}"}, "InvalidData",
                     "The field ErpID must be a string with a maximum length of 64.",
                     "Successful processing of a request with a 65-character long erpID field in body.",
                     id="Request body with 65-character long erpID field."),
    ]

    params_negative_get_warehouse_body = [
        pytest.param("test", 404, id="Sent value: test."),
        pytest.param("123test", 404, id="Sent value: 123test."),
        pytest.param("test123", 404, id="Sent value: test123."),
        pytest.param("!@#$%^&*(", 404, id="Sent value: !@#$%^&*(."),
    ]

    params_negative_add_materials_body = [
        pytest.param({
                "ErpID": f"ErpID {''.join(random.sample(string.ascii_letters + string.digits, 20))}",
                "measurementUnitID": 166,
                "Cost": 10.50,
                "costCurrencyID": 1,
                "PurchaseCost": 10.50,
                "purchaseCostCurrencyID": 1,
            }, "Create material without <name> field.", "The Name field is required.",
            id="Test create material without <name> field."),
        # pytest.param({
        #         "name": f"Материал {''.join(random.sample(string.ascii_letters + string.digits, 30))}",
        #         "ErpID": f"ErpID {''.join(random.sample(string.ascii_letters + string.digits, 30))}",
        #         "Cost": 10.50,
        #         "costCurrencyID": 1,
        #         "PurchaseCost": 10.50,
        #         "purchaseCostCurrencyID": 1,
        #     }, "Create material without <MeasurementUnitID> field.", "Неверные данные: MeasurementUnit",
        #     id="Test create material without <MeasurementUnitID> field."),
        # pytest.param({
        #         "name": f"Материал {''.join(random.sample(string.ascii_letters + string.digits, 30))}",
        #         "measurementUnitID": 166,
        #         "ErpID": f"ErpID {''.join(random.sample(string.ascii_letters + string.digits, 30))}",
        #         "Cost": 10.50,
        #         "PurchaseCost": 10.50,
        #         "purchaseCostCurrencyID": 1,
        #     }, "Create material without <CostCurrencyID> field.", "Неверные данные: Currency",
        #     id="Test create material without <CostCurrencyID> field."),
        # pytest.param({
        #         "name": f"Материал {''.join(random.sample(string.ascii_letters + string.digits, 30))}",
        #         "measurementUnitID": 166,
        #         "ErpID": f"ErpID {''.join(random.sample(string.ascii_letters + string.digits, 30))}",
        #         "Cost": 10.50,
        #         "costCurrencyID": 1,
        #         "PurchaseCost": 10.50,
        #     }, "Create material without <PurchaseCostCurrencyID> field.", "Неверные данные: PurchaseCurrency",
        #     id="Test create material without <PurchaseCostCurrencyID> field."),
        pytest.param({
                "name": "A"*129,
                "ErpID": f"ErpID {''.join(random.sample(string.ascii_letters + string.digits, 20))}",
                "measurementUnitID": 166,
                "Cost": 10.50,
                "costCurrencyID": 1,
                "PurchaseCost": 10.50,
                "purchaseCostCurrencyID": 1,
            }, "Creating material with exceeding character limits name=129.",
            "The field Name must be a string with a maximum length of 128.",
            id="Test creating material with exceeding character limits name=129."),
        # pytest.param({
        #         "name": f"Материал {random.randint(1, 99999)}",
        #         "ErpID": f"ErpID {''.join(random.sample(string.ascii_letters + string.digits, 20))}",
        #         "description": "A"*2049,
        #         "measurementUnitID": 166,
        #         "Cost": 10.50,
        #         "costCurrencyID": 1,
        #         "PurchaseCost": 10.50,
        #         "purchaseCostCurrencyID": 1,
        #     }, "Creating material with exceeding character limits description=2049.",
        #     "The field Description must be a string with a maximum length of 2048.",
        #     id="Test creating material with exceeding character limits description=2049."),
        pytest.param({
                "name": f"Материал {random.randint(1, 99999)}",
                "ErpID": f"ErpID {''.join(random.sample(string.ascii_letters + string.digits, 20))}",
                "vendorCode": "A"*33,
                "description": "Материал создан авто-тестом.",
                "measurementUnitID": 166,
                "Cost": 10.50,
                "costCurrencyID": 1,
                "PurchaseCost": 10.50,
                "purchaseCostCurrencyID": 1,
            }, "Creating material with exceeding character limits vendorCode=33.",
            "The field VendorCode must be a string with a maximum length of 32.",
            id="Test creating material with exceeding character limits vendorCode=33."),
        pytest.param({
                "name": f"Материал {random.randint(1, 99999)}",
                "ErpID": "A"*65,
                "vendorCode": f"Code {random.randint(1, 99999)}",
                "description": "Материал создан авто-тестом.",
                "measurementUnitID": 166,
                "Cost": 10.50,
                "costCurrencyID": 1,
                "PurchaseCost": 10.50,
                "purchaseCostCurrencyID": 1,
            }, "Creating material with exceeding character limits erpID=65.",
            "The field ErpID must be a string with a maximum length of 64.",
            id="Test creating material with exceeding character limits erpID=65.")
    ]

    params_negative_update_material_body = [
        pytest.param({
                "ErpID": f"ErpID {''.join(random.sample(string.ascii_letters + string.digits, 20))}",
                "measurementUnitID": 166,
                "Cost": 10.50,
                "costCurrencyID": 1,
                "PurchaseCost": 10.50,
                "purchaseCostCurrencyID": 1,
            }, "Update material without <name> field.", "The Name field is required.",
            id="Test update material without <name> field."),
        # pytest.param({
        #         "name": f"Материал {random.randint(1, 99999)}",
        #         "ErpID": f"ErpID {''.join(random.sample(string.ascii_letters + string.digits, 20))}",
        #         "Cost": 10.50,
        #         "costCurrencyID": 1,
        #         "PurchaseCost": 10.50,
        #         "purchaseCostCurrencyID": 1,
        #     }, "Update material without <MeasurementUnitID> field.", "Неверные данные: MeasurementUnit",
        #     id="Test update material without <MeasurementUnitID> field."),
        # pytest.param({
        #         "name": f"Материал {random.randint(1, 99999)}",
        #         "measurementUnitID": 166,
        #         "ErpID": f"ErpID {''.join(random.sample(string.ascii_letters + string.digits, 20))}",
        #         "Cost": 10.50,
        #         "PurchaseCost": 10.50,
        #         "purchaseCostCurrencyID": 1,
        #     }, "Update material without <CostCurrencyID> field.", "Неверные данные: Currency",
        #     id="Test update material without <CostCurrencyID> field."),
        # pytest.param({
        #         "name": f"Материал {random.randint(1, 99999)}",
        #         "measurementUnitID": 166,
        #         "ErpID": f"ErpID {''.join(random.sample(string.ascii_letters + string.digits, 20))}",
        #         "Cost": 10.50,
        #         "costCurrencyID": 1,
        #         "PurchaseCost": 10.50,
        #     }, "Update material without <PurchaseCostCurrencyID> field.", "Неверные данные: PurchaseCurrency",
        #     id="Test update material without <PurchaseCostCurrencyID> field."),
        pytest.param({
                "name": "A"*129,
                "ErpID": f"ErpID {''.join(random.sample(string.ascii_letters + string.digits, 20))}",
                "measurementUnitID": 166,
                "Cost": 10.50,
                "costCurrencyID": 1,
                "PurchaseCost": 10.50,
                "purchaseCostCurrencyID": 1,
            }, "Update material with exceeding character limits name=129.",
            "The field Name must be a string with a maximum length of 128.",
            id="Test update material with exceeding character limits name=129."),
        # pytest.param({
        #         "name": f"Материал {random.randint(1, 99999)}",
        #         "ErpID": f"ErpID {''.join(random.sample(string.ascii_letters + string.digits, 20))}",
        #         "description": "A"*2049,
        #         "measurementUnitID": 166,
        #         "Cost": 10.50,
        #         "costCurrencyID": 1,
        #         "PurchaseCost": 10.50,
        #         "purchaseCostCurrencyID": 1,
        #     }, "Update material with exceeding character limits description=2049.",
        #     "The field Description must be a string with a maximum length of 2048.",
        #     id="Test update material with exceeding character limits description=2049."),
        pytest.param({
                "name": f"Материал {random.randint(1, 99999)}",
                "ErpID": f"ErpID {''.join(random.sample(string.ascii_letters + string.digits, 20))}",
                "vendorCode": "A"*33,
                "description": "Материал создан авто-тестом.",
                "measurementUnitID": 166,
                "Cost": 10.50,
                "costCurrencyID": 1,
                "PurchaseCost": 10.50,
                "purchaseCostCurrencyID": 1,
            }, "Update material with exceeding character limits vendorCode=33.",
            "The field VendorCode must be a string with a maximum length of 32.",
            id="Test update material with exceeding character limits vendorCode=33."),
        pytest.param({
                "name": f"Материал {random.randint(1, 99999)}",
                "ErpID": "A"*65,
                "vendorCode": f"Code {random.randint(1, 99999)}",
                "description": "Материал создан авто-тестом.",
                "measurementUnitID": 166,
                "Cost": 10.50,
                "costCurrencyID": 1,
                "PurchaseCost": 10.50,
                "purchaseCostCurrencyID": 1,
            }, "Update material with exceeding character limits erpID=65.",
            "The field ErpID must be a string with a maximum length of 64.",
            id="Test update material with exceeding character limits erpID=65.")
    ]

    params_negative_add_package_body = [
        pytest.param({
            "Version": f"{random.randint(0, 9)}.{random.randint(0, 99)}.{random.randint(1, 99)}",
            "Name": f"Name {random.randint(1, 999999)}",
            "IconUrl": "https://239911.selcdn.ru/Plugins/default.png",
            "AddonUrl": "https://ya.ru/",
            "ResourceID": 1,
            "IsMobile": False
        },
            "Add a package by cross tenant admin to database without AddonID field.",
            "Параметр [AddonID] не может быть пустым.",
            id="Test add package without <AddonID> field."),
        pytest.param({
            "AddonID": f"{random.randint(1, 999999999999)}",
            "Name": f"Name {random.randint(1, 999999)}",
            "IconUrl": f"https://dev-automate.hubex.ru/webhook/{random.randint(1, 9999999)}",
            "AddonUrl": "https://ya.ru/",
            "ResourceID": 1,
            "IsMobile": False
        },
            "Add a package by cross tenant admin to database without Version field.",
            "Параметр [Version] не может быть пустым.",
            id="Test add package without <Version> field."),
        pytest.param({
            "AddonID": f"{random.randint(1, 999999999999)}",
            "Version": f"{random.randint(0, 9)}.{random.randint(0, 99)}.{random.randint(1, 99)}",
            "IconUrl": "https://239911.selcdn.ru/Plugins/default.png",
            "AddonUrl": "https://ya.ru/",
            "ResourceID": 1,
            "IsMobile": False
        },
            "Add a package by cross tenant admin to database without Name field.",
            "Параметр [Name] не может быть пустым.",
            id="Test add package without <Name> field."),
        pytest.param({
            "AddonID": f"{random.randint(1, 999999999999)}",
            "Version": f"{random.randint(0, 9)}.{random.randint(0, 99)}.{random.randint(1, 99)}",
            "Name": "",
            "IconUrl": f"https://dev-automate.hubex.ru/webhook/{random.randint(1, 9999999)}",
            "AddonUrl": "https://ya.ru/",
            "ResourceID": 1,
            "IsMobile": False
        },
            "Add a package by cross tenant admin to database with empty string in Name field.",
            "Параметр [Name] не может быть пустым.",
            id="Test add package with empty string in <Name> field."),
        pytest.param({
            "AddonID": f"{random.randint(1, 999999999999)}",
            "Version": f"{random.randint(0, 9)}.{random.randint(0, 99)}.{random.randint(1, 99)}",
            "Name": f"Name {random.randint(1, 999999)}",
            "AddonUrl": "https://ya.ru/",
            "ResourceID": 1,
            "IsMobile": False
        },
            "Add a package by cross tenant admin to database without IconUrl field.",
            "Параметр [IconUrl] не может быть пустым.",
            id="Test add package without <IconUrl> field."),
        pytest.param({
            "AddonID": f"{random.randint(1, 999999999999)}",
            "Version": f"{random.randint(0, 9)}.{random.randint(0, 99)}.{random.randint(1, 99)}",
            "Name": f"Name {random.randint(1, 999999)}",
            "IconUrl": "https://ya.ru/",
            "ResourceID": 1,
            "IsMobile": False
        },
            "Add a package by cross tenant admin to database without AddonUrl field.",
            "Параметр [AddonUrl] не может быть пустым.",
            id="Test add package without <AddonUrl> field."),
        pytest.param({
            "AddonID": f"{random.randint(1, 999999999999)}",
            "Version": f"{random.randint(0, 9)}.{random.randint(0, 99)}.{random.randint(1, 99)}",
            "Name": f"Name {random.randint(1, 999999)}",
            "IconUrl": "https://239911.selcdn.ru/Plugins/default.png",
            "AddonUrl": "https://ya.ru/",
            "IsMobile": False
        },
            "Add a package by cross tenant admin to database without ResourceID field.",
            "Параметр [ResourceID] не может быть пустым.",
            id="Test add package without <ResourceID> field.")
    ]

    params_add_package_to_different_resource_body = [
        pytest.param(1, "Форма заявки", "Add package with ResourceID=1", False,
                     id="Test add package with ResourceID=1, TaskForm."),
        pytest.param(2, "Список заявок", "Add package with ResourceID=2", False,
                     id="Test add package with ResourceID=2, TasksList."),
        pytest.param(3, "Форма сотрудника", "Add package with ResourceID=3", False,
                     id="Test add package with ResourceID=3, TechnicianForm."),
        pytest.param(4, "Список сотрудников", "Add package with ResourceID=4", False,
                     id="Test add package with ResourceID=4, TechniciansList."),
        pytest.param(5, "Форма заказчиков", "Add package with ResourceID=5", False,
                     id="Test add package with ResourceID=5, CustomerForm."),
        pytest.param(6, "Список заказчиков", "Add package with ResourceID=6", False,
                     id="Test add package with ResourceID=6, CustomersList."),
        pytest.param(7, "AssetForm", "Add package with ResourceID=7", False,
                     id="Test add package with ResourceID=7, AssetForm."),
        pytest.param(8, "AssetsList", "Add package with ResourceID=8", False,
                     id="Test add package with ResourceID=8, AssetsList."),
        pytest.param(9, "Страница аналитики", "Add package with ResourceID=9", False,
                     id="Test add package with ResourceID=9, Analytics."),
        pytest.param(10, "Страница PowerBI-отчета",
                     "Add package with ResourceID=10", False,
                     id="Test add package with ResourceID=10, PowerBIReport."),
        pytest.param(11, "Подпункт в форме заявки",
                     "Add package with ResourceID=11", False,
                     id="Test add package with ResourceID=11, SubitemTask."),
        pytest.param(12, "Подпункт в форме объекта",
                     "Add package with ResourceID=12", False,
                     id="Test add package with ResourceID=12, SubitemAsset."),
        pytest.param(13, "Подпункт в форме сотрудника",
                     "Add package with ResourceID=13", False,
                     id="Test add package with ResourceID=13, SubitemTechnician."),
        pytest.param(14, "Подпункт в форме заказчика",
                     "Add package with ResourceID=14", False,
                     id="Test add package with ResourceID=14, SubitemCustomer."),
        pytest.param(15, "Подпункт в форме компании",
                     "Add package with ResourceID=15", False,
                     id="Test add package with ResourceID=15, SubitemCompany."),
        pytest.param(16, "Подпункт меню в меню Заявки",
                     "Add package with ResourceID=16", False,
                     id="Test add package with ResourceID=16, SubitemMenuTask."),
        pytest.param(17, "Подпункт меню в меню Объекты",
                     "Add package with ResourceID=17", False,
                     id="Test add package with ResourceID=17, SubitemMenuAsset."),
        pytest.param(18, "Подпункт меню в меню Пользователи",
                     "Add package with ResourceID=18", False,
                     id="Test add package with ResourceID=18, SubitemMenuUser."),
        pytest.param(19, "Подпункт меню в меню Компании",
                     "Add package with ResourceID=19", False,
                     id="Test add package with ResourceID=19, SubitemMenuCompany."),
        pytest.param(20, "Подпункт меню в меню Аналитика",
                     "Add package with ResourceID=20", False,
                     id="Test add package with ResourceID=20, SubitemMenuAnalytics."),
        pytest.param(21, "Подпункт меню в меню Карты",
                     "Add package with ResourceID=21", False,
                     id="Test add package with ResourceID=21, SubitemMenuMap."),
        pytest.param(22, "Подпункт меню в меню Склады",
                     "Add package with ResourceID=22", False,
                     id="Test add package with ResourceID=22, SubitemMenuWarehouse."),
        pytest.param(23, "Новый пункт меню",
                     "Add package with ResourceID=2", False,
                     id="Test add package with ResourceID=23, NewMenuItem."),
        pytest.param(24, "Пункт меню в мобильном приложении",
                     "Add package with ResourceID=24", True,
                     id="Test add package with ResourceID=24, MenuItemMA."),
        pytest.param(25, "Новый подпункт в заявке в мобильном приложении",
                     "Add package with ResourceID=25", True,
                     id="Test add package with ResourceID=25, NewSubitemTaskMA."),
        pytest.param(26, "Новый подпункт в списке заявок в мобильном приложении",
                     "Add package with ResourceID=26", True,
                     id="Test add package with ResourceID=26, NewSubitemTaskListMA."),
    ]

    params_user_attributes_body = [
        pytest.param(1, "Строка", id="Test add string attribute to user."),
        pytest.param(2, 123, id="Test add Int attribute to user."),
        pytest.param(3, 1.2, id="Test add Decimal attribute to user."),
        pytest.param(4, "2030-09-18T12:00:00", id="Test add Date attribute to user."),
        pytest.param(5, "2030-09-18T20:59:00.000Z", id="Test add Datetime attribute to user."),
        pytest.param(6, "1", id="Test add Select attribute to user"),
        pytest.param(7, "1|2|3", id="Test add MultiSelect attribute to user."),
        pytest.param(8, "Объективное\nизложение\nфактов\nбез\nэмоциональной\nокраски\nи\nсубъективных\nпредпочтений", 
                     id="Test add Text attribute to user.")
    ]

    params_user_attributes_by_id_body = [
        pytest.param(1, "Строка", id="Test add string attribute to user, by userID."),
        pytest.param(2, 123, id="Test add Int attribute to user, by userID."),
        pytest.param(3, 1.2, id="Test add Decimal attribute to user, by userID."),
        pytest.param(4, "2030-09-18T12:00:00", id="Test add Date attribute to user, by userID."),
        pytest.param(5, "2030-09-18T20:59:00.000Z", id="Test add Datetime attribute to user, by userID."),
        pytest.param(6, "1", id="Test add Select attribute to user, by userID."),
        pytest.param(7, "1|2|3", id="Test add MultiSelect attribute to user, by userID."),
        pytest.param(8, "Объективное\nизложение\nфактов\nбез\nэмоциональной\nокраски\nи\nсубъективных\nпредпочтений", 
                     id="Test add Text attribute to user, by userID.")
    ]

    params_update_user_attributes_body = [
        pytest.param(1, "Строка", "Изменено авто-тестом", id="Test update string users attribute."),
        pytest.param(2, 123, "987", id="Test update Int users attribute."),
        pytest.param(3, 1.2, "3.4", id="Test update Decimal users attribute."),
        pytest.param(4, "2030-09-18T12:00:00", "2031-10-18T12:00:00", id="Test update Date users attribute."),
        pytest.param(5, "2030-09-18T20:59:00.000Z", "2031-10-18T21:59:10.000Z", id="Test update Datetime users attribute."),
        pytest.param(6, "1", "2", id="Test update Select users attribute"),
        pytest.param(7, "1|2", "3|4", id="Test update MultiSelect users attribute."),
        pytest.param(8, "Объективное\nизложение\nфактов\nбез\nэмоциональной\nокраски\nи\nсубъективных\nпредпочтений",
                     "Текст\nизменен\nавто-тестом\nбыстро\nи без ошибок", 
                     id="Test update Text users attribute.")
    ]

    params_content_type_body = [
        pytest.param("text/plain", id="Test get list geolocation settings with content type text/plain."),
        pytest.param("application/json", id="Test get list geolocation settings with content type application/json."),
        pytest.param("text/json", id="Test get list geolocation settings with content type text/json.")
    ]
