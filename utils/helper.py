import allure
import json
from allure_commons.types import AttachmentType


class Helper:

    @classmethod
    def attach_response(cls, response):
        response = json.dumps(response, indent=4)
        allure.attach(body=response, name='API Response', attachment_type=AttachmentType.JSON)

    @classmethod
    def attach_request(cls, request):
        allure.attach(body=request, name='API Request body', attachment_type=AttachmentType.JSON)

    @classmethod
    def attach_time(cls, start_time, end_time):
        response_time_ms = (end_time - start_time) * 1000
        allure.attach(f'API Response time: {response_time_ms:.2f}ms', name="Response Time",
                      attachment_type=AttachmentType.JSON)
