import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Common service offers various methods for managing common and auxiliary dictionaries.")
class TestCommonPowerBIReports(BaseTest):

    # @allure.title('Test get list power BI reports.')
    # @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25697")
    # @pytest.mark.regress
    # @pytest.mark.test_case_id(25697)
    # @pytest.mark.skip(reason="Тест на получения списка power BI отчетов проходит в - test_get_power_bi_report_by_id")
    # def test_get_list_power_bi_reports(self):
    #     self.api_common_power_bi_reports.get_list_power_bi_reports()

    @allure.title('Test get power BI report by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25698")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25698)
    def test_get_power_bi_report_by_id(self):
        model = self.api_common_power_bi_reports.get_list_power_bi_reports()
        self.api_common_power_bi_reports.get_power_bi_report_by_id(model.results[0].id)
