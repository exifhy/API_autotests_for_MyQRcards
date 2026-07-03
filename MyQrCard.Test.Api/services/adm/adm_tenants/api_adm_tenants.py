import random
import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.adm.adm_tenants.payloads import Payloads
from services.adm.adm_tenants.endpoints import Endpoints
from config.headers import Headers
from services.adm.adm_tenants.models.adm_tenants_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class AdmTenantsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Get data current tenant.")
    def get_data_current_tenant(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_data_current_tenant_endpoint,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.warning(f"Status code:{HTTPStatus.NO_CONTENT}, no current tenant data.")
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = SuccessGetCurrentOwnerTenantResult(**response.json())
        logger.success(f'Successfully get data current tenant.')
        return model

    @allure.step("Get list of tenants to which the authorized user has access.")
    def get_list_tenants(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_tenants_endpoint,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.warning(f"Status code:{HTTPStatus.NO_CONTENT}, no list tenants.")
            return None
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {(HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT)}, '
             f'but got {response.status_code}, {data_response}')
        model = SuccessGetListTenantsListResult(results=response.json())
        logger.success(f'Successfully get list of tenants to which the authorized user has access.')
        return model

    @allure.step("Get list of template tenants to which the authenticated user has access.")
    def get_list_templates_tenants(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_templates_tenants_endpoint,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.warning(f"Status code:{HTTPStatus.NO_CONTENT}, no list templates tenants.")
            return None
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {(HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT)}, '
             f'but got {response.status_code}, {data_response}')
        model = SuccessGetListTemplatesITenantEntityModel(results=response.json())
        logger.success(f'Successfully get list of templates tenants to which the authenticated user has access.')
        return model

    @allure.step("Get list of feature flags tenants.")
    def get_list_feature_flags_tenants(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_feature_flags_tenants_endpoint,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.warning(f"Status code:{HTTPStatus.NO_CONTENT}, no list feature flags tenants.")
            return None
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {(HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT)}, '
             f'but got {response.status_code}, {data_response}')
        model = SuccessGetListFeatureFlagsForTenantModel(results=response.json())
        logger.success(f'Successfully get list of feature flags tenants.')
        return model

    @allure.step("Get list of licenses tenants.")
    def get_list_of_licenses_tenants(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_licenses_tenant_endpoint,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.warning(f"Status code:{HTTPStatus.NO_CONTENT}, no list of licenses tenants.")
            return None
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {(HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT)}, '
             f'but got {response.status_code}, {data_response}')
        model = SuccessGetListTenantLicenseResultModel(results=response.json())
        logger.success(f'Successfully get list of licenses tenants.')
        return model

    @allure.step("Add license and payment info to tenant.")
    def post_add_license_to_tenant(self):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_license_tenant_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_license_tenant_payload()
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        logger.success(f'Successfully add license and payment info to tenant.')
        return None

    @allure.step("Delete license from tenant by list.")
    def delete_licenses_from_tenant_by_list(self, *licenses_ids: int | tuple):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_licenses_from_tenant_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_licenses_from_tenant_by_list_payload(*licenses_ids)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        logger.success(f'Successfully delete license from tenant by list {licenses_ids}.')
        return None

    @allure.step("Delete license from tenant by id.")
    def delete_licenses_from_tenant_by_list(self, licenses_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_license_from_tenant_by_id_endpoint(licenses_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        logger.success(f'Successfully delete license from tenant by ID {licenses_id}.')
        return None

    @allure.step("Sending a license renewal request.")
    def post_renewal_licenses_tenant(self):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_renewal_license_tenant_endpoint,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        logger.success(f'Successfully sending a license renewal request.')
        return None

    @allure.step("Update a licenses for tenant.")
    def put_update_licenses_for_tenant(self):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_license_tenant_endpoint,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        logger.success(f'Successfully sending a license renewal request.')
        return None

    @allure.step("Get a list meta from tenant.")
    def get_list_meta_from_tenant(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_meta_from_tenant_endpoint,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.warning(f"Status code:{HTTPStatus.NO_CONTENT}, no list of meta tenants.")
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        logger.success(f'Successfully get a list meta from tenant.')
        return None

    @allure.step("Get list packages from tenant.")
    def get_list_packages_from_tenant(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_packages_from_tenant_endpoint,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.warning(f"Status code:{HTTPStatus.NO_CONTENT}, no list of packages tenants.")
            return None
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {(HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT)}, '
             f'but got {response.status_code}, {data_response}')
        model = SuccessGetTenantPackagesListResultModel(results=response.json())
        logger.success(f'Successfully get a list packages from tenant.')
        return model

    @allure.step("Add a package by cross tenant admin to database with the isMobile field, ResourceID=24.")
    def post_add_packages_to_data_base_cross_tenant_admin_with_is_mobile_field(self, token: str):
        data = {
            "AddonID": f"{random.randint(1, 999999999999)}",
            "Version": f"{random.randint(0, 9)}.{random.randint(0, 99)}.{random.randint(1, 99)}",
            "Name": f"Name {random.randint(1, 999999)}",
            "IconUrl": "https://239911.selcdn.ru/Plugins/default.png",
            "AddonUrl": "https://ya.ru/",
            "ResourceID": 23,
            "IsMobile": True
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_packages_to_db_cross_tenant_admin_endpoint,
            headers=self.headers.basic_header(token),
            json=data
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = SuccessGetTenantPackagesListResultModel(results=response.json())
        logger.success(f'Successfully add packages ID {model.results[0].package.id} to data base with isMobile field.')
        return model

    @allure.step("Add a package by cross tenant admin to database without the isMobile field.")
    def post_add_packages_to_data_base_cross_tenant_admin_without_mobile_field(self, token: str):
        data = {
            "AddonID": f"{random.randint(1, 999999999999)}",
            "Version": f"{random.randint(0, 9)}.{random.randint(0, 99)}.{random.randint(1, 99)}",
            "Name": f"Name {random.randint(1, 999999)}",
            "IconUrl": "https://239911.selcdn.ru/Plugins/default.png",
            "AddonUrl": "https://ya.ru/",
            "ResourceID": 1
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_packages_to_db_cross_tenant_admin_endpoint,
            headers=self.headers.basic_header(token),
            json=data
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = SuccessGetTenantPackagesListResultModel(results=response.json())
        logger.success(f'Successfully add packages ID {model.results[0].package.id} to data base without isMobile field.')
        return model

    @allure.step("Add a package by cross tenant admin to system with str in ResourceID filed.")
    def post_add_packages_to_sys_cross_tenant_admin_with_str_in_resource_id_field(self, token: str):
        """resourceID = integer($int32) по схеме."""
        data = {
            "AddonID": f"{random.randint(1, 999999999999)}",
            "Version": f"{random.randint(0, 9)}.{random.randint(0, 99)}.{random.randint(1, 99)}",
            "Name": f"Name {random.randint(1, 999999)}",
            "IconUrl": "https://239911.selcdn.ru/Plugins/default.png",
            "AddonUrl": "https://ya.ru/",
            "ResourceID": "1",
            "IsMobile": False
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_packages_to_db_cross_tenant_admin_endpoint,
            headers=self.headers.basic_header(token),
            json=data
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.OK:
            model = SuccessGetTenantPackagesListResultModel(results=response.json())
            logger.warning(f"Status code:{response.status_code}, created packages tenants.")
            return model
        else:
            assert response.status_code == HTTPStatus.CONFLICT, \
                f'Expected status code {HTTPStatus.CONFLICT}, but got {response.status_code}, {data_response}'
            model = ErrorModel(results=response.json())
            logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}')
            return None

    @allure.step("Add a package without Authorization header.")
    def post_add_package_without_authorization(self):
        data = {
            "AddonID": f"{random.randint(1, 999999999999)}",
            "Version": f"{random.randint(0, 9)}.{random.randint(0, 99)}.{random.randint(1, 99)}",
            "Name": f"Name {random.randint(1, 999999)}",
            "IconUrl": "https://239911.selcdn.ru/Plugins/default.png",
            "AddonUrl": "https://ya.ru/",
            "ResourceID": 1,
            "IsMobile": False
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_packages_to_db_cross_tenant_admin_endpoint,
            headers=self.headers.basic_header_without_authorization,
            json=data
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.UNAUTHORIZED, \
            f'Expected status code {HTTPStatus.UNAUTHORIZED}, but got {response.status_code}, {data_response}'
        logger.warning(f'Expected result: error {response.status_code}, message: Unauthorized')
        return None

    def post_add_package_to_database_without_fields(self, token: str, data: dict, name_step: str, error_message: str):
        with allure.step(name_step):
            start = time.time()
            response = requests.post(
                url=self.endpoints.post_add_packages_to_db_cross_tenant_admin_endpoint,
                headers=self.headers.basic_header(token),
                json=data
            )
            end = time.time()
            logger.info(response.headers)
            self.attach_response_headers(response.headers)
            data_response = self.response_content(response)
            self.attach_response(data_response)
            self.attach_time(start, end)
            self.attach_request(response.request.body)
            self.attach_url(response.request.url)
            assert response.status_code == HTTPStatus.CONFLICT, \
                f'Expected status code {HTTPStatus.CONFLICT}, but got {response.status_code}, {data_response}'
            model = ErrorModel(results=response.json())
            assert model.results[0].code == "ParameterNull", \
                f'Expected <ParameterNull>, but got {model.results[0].code}'
            assert model.results[0].message == error_message, \
                f'Expected {error_message}, but got {model.results[0].message}'
            assert "ParameterNull" in response.headers["X-Application-Errors"], \
                f'Expected <ParameterNull>, but got {response.headers["X-Application-Errors"]}'
            logger.warning(f'Expected result: error {response.status_code}, message: {model.results[0].message}')
            return None

    @allure.step("Delete packages from system.")
    def delete_packages_from_system(self, token: str, addon_id: str, version: str):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_packages_from_db_cross_tenant_admin_endpoint,
            headers=self.headers.basic_header(token),
            json=self.payloads.delete_packages_from_db_payload(addon_id, version)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        logger.success(f'Successfully delete packages from database ID {addon_id}.')

    @allure.step("Delete packages from system without Version field.")
    def delete_packages_from_system_without_version_field(self, token: str, addon_id: str):
        data = {
            "addonID": addon_id
        }
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_packages_from_db_cross_tenant_admin_endpoint,
            headers=self.headers.basic_header(token),
            json=data
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CONFLICT, \
            f'Expected status code {HTTPStatus.CONFLICT}, but got {response.status_code}, {data_response}'
        model = ErrorModel(results=response.json())
        assert model.results[0].code == "ParameterNull", \
            f'Expected <ParameterNull>, but got {model.results[0].code}'
        assert model.results[0].message == "Параметр [Version] не может быть пустым.", \
            f'Expected Параметр [Version] не может быть пустым., but got {model.results[0].message}'
        assert "ParameterNull" in response.headers["X-Application-Errors"], \
            f'Expected <ParameterNull>, but got {response.headers["X-Application-Errors"]}'
        logger.warning(f'Expected result: error {response.status_code}, message: {model.results[0].message}')
        return None

    @allure.step("Add a already exists package by cross tenant admin to system.")
    def post_add_packages_to_system_cross_tenant_admin_already_exists(self, token: str, addon_id: str, version: str):
        data = {
            "AddonID": addon_id,
            "Version": version,
            "Name": f"Name {random.randint(1, 999999)}",
            "IconUrl": "https://239911.selcdn.ru/Plugins/default.png",
            "AddonUrl": "https://ya.ru/",
            "ResourceID": 1,
            "IsMobile": False
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_packages_to_db_cross_tenant_admin_endpoint,
            headers=self.headers.basic_header(token),
            json=data
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CONFLICT, \
            f'Expected status code {HTTPStatus.CONFLICT}, but got {response.status_code}, {data_response}'
        model = ErrorModel(results=response.json())
        assert model.results[0].code == "AlreadyExists", \
            f'Expected <AlreadyExists>, but got {model.results[0].code}'
        assert model.results[0].message == "Уже существует", \
            f'Expected <Уже существует>, but got {model.results[0].message}'
        assert "AlreadyExists" in response.headers["X-Application-Errors"], \
            f'Expected <AlreadyExists>, but got {response.headers["X-Application-Errors"]}'
        logger.warning(f'Expected result: error {response.status_code}, message: {model.results[0].message}')
        return None

    @allure.step("Patch update a package by cross tenant admin.")
    def patch_update_package_cross_tenant_admin(self, token: str, addon_id: str):
        data = {
            "AddonID": addon_id,
            "Version": f"{random.randint(0, 99)}.{random.randint(0, 99)}.{random.randint(1, 99)}",
            "Name": f"Updated name {random.randint(1, 999999)}"
        }
        start = time.time()
        response = requests.patch(
            url=self.endpoints.patch_packages_db_cross_tenant_admin_endpoint,
            headers=self.headers.basic_header(token),
            json=data
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        logger.success(f'Successfully patch update system package ID {addon_id}.')

    def post_add_package_to_database_with_all_resource(
            self, token: str, resource_id: int, name: str, name_step: str, mobile: bool):
        with allure.step(name_step):
            data = {
                "AddonID": f"{random.randint(1, 99999999999999999)}",
                "Version": f"{random.randint(0, 9)}.{random.randint(0, 99)}.{random.randint(1, 99)}",
                "Name": name,
                "IconUrl": "https://239911.selcdn.ru/Plugins/default.png",
                "AddonUrl": "https://ya.ru/",
                "ResourceID": resource_id,
                "IsMobile": mobile
            }
            start = time.time()
            response = requests.post(
                url=self.endpoints.post_add_packages_to_db_cross_tenant_admin_endpoint,
                headers=self.headers.basic_header(token),
                json=data
            )
            end = time.time()
            logger.info(response.headers)
            self.attach_response_headers(response.headers)
            data_response = self.response_content(response)
            self.attach_response(data_response)
            self.attach_time(start, end)
            self.attach_request(response.request.body)
            self.attach_url(response.request.url)
            assert response.status_code == HTTPStatus.OK, \
                f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
            model = SuccessGetTenantPackagesListResultModel(results=response.json())
            logger.success(f'Successfully add system package by cross tenant admin.')
            return model

    @allure.step("Add a package to tenant.")
    def post_add_package_to_tenant(self, addon_id: str, version: str, mobile: bool):
        data = {
            "AddonID": addon_id,
            "Version": version,
            "IsMobile": mobile
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_packages_to_tenant_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=data
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = SuccessGetTenantPackagesListResultModel(results=response.json())
        assert model.results[0].package.id == addon_id, "Плагин не добавился к тенанту."
        assert model.results[0].package.version == version, "Плагин не добавился к тенанту."
        logger.success(f'Successfully add package to tenant ID {addon_id}.')
        return model

    @allure.step("Delete a package from tenant.")
    def delete_package_from_tenant(self, addon_id: str, version: str):
        data = {
            "AddonID": addon_id,
            "Version": version
        }
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_packages_from_tenant_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=data
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        logger.success(f'Successfully delete package from tenant by ID {addon_id}.')

    @allure.step("Get a list variables from tenant.")
    def get_list_variables_from_tenant(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_variables_from_tenant_endpoint,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.warning(f"Status code:{HTTPStatus.NO_CONTENT}, no list of variables tenant.")
            return None
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {(HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT)}, '
             f'but got {response.status_code}, {data_response}')
        model = SuccessGetListTenantVariablesResultModel(root=response.json())
        logger.success(f'Successfully get a list variables from tenant.')
        return model

    @allure.step("Add variables to tenant.")
    def post_add_variables_to_tenant(self) -> str:
        name = f"Variable{random.randint(1, 99999)}"
        data = {
            "name": name,
            "value": f"Значение{random.randint(1, 99999)}",
            "description": "Переменная окружения создана авто-тестом"
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_variables_to_tenant_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_variables_to_tenant_payload(data)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        logger.success(f'Successfully add variables to tenant with name {name}.')
        return name

    @allure.step("Update variables tenant.")
    def put_update_variables_tenant(self, name: str):
        model_before = self.get_list_variables_from_tenant()
        data = {
            "name": name,
            "value": f"Обновленное {random.randint(1, 99999)}",
            "description": "Переменная окружения обновлена авто-тестом"
        }
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_variables_tenant_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_update_variables_tenant_payload(data)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        name_variable = name.lower()
        model_after = self.get_list_variables_from_tenant()
        assert model_before.root[name_variable].value != model_after.root[name_variable].value, \
            (f"{model_before.root[name_variable].value} is equal "
             f"{model_after.root[name_variable].value}. Variable not updated.")
        assert model_before.root[name_variable].description != model_after.root[name_variable].description, \
            (f"{model_before.root[name_variable].description} is equal "
             f"{model_after.root[name_variable].description}. Variable not updated.")
        logger.success(f'Successfully update variables tenant with name {name}.')

    @allure.step("Delete variables from tenant by list.")
    def delete_variables_from_tenant_by_list(self, *names: str | tuple):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_variables_from_tenant_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_variables_from_tenant_payload(*names)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        logger.success(f'Successfully delete variables from tenant by names:{names}.')

    @allure.step("Delete variable from tenant by name.")
    def delete_variable_from_tenant_by_name(self, name: str):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_variables_from_tenant_by_name_endpoint(name),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        logger.success(f'Successfully delete variables from tenant by name: {name}.')


