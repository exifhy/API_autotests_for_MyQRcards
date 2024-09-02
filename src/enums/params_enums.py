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
