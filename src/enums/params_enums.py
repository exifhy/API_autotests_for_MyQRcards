from enum import Enum
import pytest


class Params(Enum):

    params_user = [
        pytest.param('', id=""),
        pytest.param('', id="")
    ]
