import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Data Export Service")
@allure.feature("Export users data")
class TestExportUsers(BaseTest):

    @allure.title('Test exports the list of users taking into account the specified filters by userID(Customers).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23172")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23172)
    def test_get_export_list_customers_by_user_id(self):
        customer_model = self.api_adm_users.post_add_user_customer()
        user_info = self.api_adm_users.get_user_info_by_id(customer_model.userID)
        created_company_id = self.api_es_companies.post_add_our_company()
        company_model = self.api_es_companies.get_detailed_information_on_company_by_id(created_company_id)
        district_model = self.api_es_districts.post_add_district()
        district_info = self.api_es_districts.get_detail_district_info_by_id(district_model.districts[0])
        self.api_pa_employment.post_add_user_employment_by_id(
            user_id=customer_model.userID,
            customer_org_unit_id=company_model.customerOrgUnit.id
        )
        model_roles = self.api_adm_roles.get_list_roles_undeleted()
        self.api_adm_user_roles.post_add_roles_to_user(customer_model.userID, model_roles.results[0].id)
        self.api_adm_user_districts.post_add_districts_to_user(district_model.districts[0], customer_model.userID)
        model_user_roles = self.api_adm_users.get_users_roles_by_id(customer_model.userID)
        self.api_export_users.get_export_list_customers_by_user_id(
            user_id=customer_model.userID,
            name=user_info.firstName,
            surname=user_info.lastName,
            email=user_info.email,
            phone=user_info.mobilePhone,
            role=model_user_roles.root[str(customer_model.userID)][0].name,
            district_name=district_info.name,
            company_name=company_model.name
        )
        self.api_adm_users.delete_user_by_id(customer_model.userID)
        self.api_es_companies.delete_company_by_id(created_company_id)
        self.api_es_districts.delete_district_by_id(district_model.districts[0])

    @allure.title('Test exports the list of users taking into account the specified filters by userID(Staff).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23173")
    @pytest.mark.smoke
    def test_get_export_list_staff_by_user_id(self):
        staff_model = self.api_adm_users.post_add_user_staff()
        user_info = self.api_adm_users.get_user_info_by_id(staff_model.userID)
        model_roles = self.api_adm_roles.get_list_roles_undeleted()
        self.api_adm_user_roles.post_add_roles_to_user(staff_model.userID, model_roles.results[0].id)
        district_model = self.api_es_districts.post_add_district()
        self.api_adm_user_districts.post_add_districts_to_user(district_model.districts[0], staff_model.userID)
        model_user_roles = self.api_adm_users.get_users_roles_by_id(staff_model.userID)
        district_info = self.api_es_districts.get_detail_district_info_by_id(district_model.districts[0])
        self.api_export_users.get_export_list_staff_by_user_id(
            user_id=staff_model.userID,
            name=user_info.firstName,
            surname=user_info.lastName,
            email=user_info.email,
            phone=user_info.mobilePhone,
            role=model_user_roles.root[str(staff_model.userID)][0].name,
            district_name=district_info.name,
            technician=user_info.isTechnician
        )
        self.api_adm_users.delete_user_by_id(staff_model.userID)
        self.api_es_districts.delete_district_by_id(district_model.districts[0])
