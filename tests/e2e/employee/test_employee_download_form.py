import allure
import pytest
from http import HTTPStatus


@allure.epic("LK")
@allure.feature("Employee")
@allure.title("Download employment form")
@pytest.mark.employee
@pytest.mark.export
def test_employee_download_form(lk_api, cfg):
    """
    GET /exports/employment?noData=true
    Должен вернуть XLSX файл.
    """

    headers = dict(lk_api.session.headers)
    headers.pop("Content-Type", None)
    headers["Accept"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    headers["Accept-Language"] = "ru-RU"
    headers["User-Agent"] = "PostmanRuntime/7.51.0"
    headers["X-Aplication-ID"] = str(cfg.get("x_application_id") or "3")

    candidates = [
        "/exports/employment?noData=true",
        "/exports/employment?noData=false",
    ]

    last = None
    for path in candidates:
        with allure.step(f"GET {path}"):
            response = lk_api.session.get(
                lk_api.base_url + path,
                headers=headers,
                allow_redirects=True,
                timeout=30,
            )
            last = response

        if response.status_code == HTTPStatus.OK and response.content:
            allure.attach(
                response.headers.get("content-type", ""),
                "content_type",
                allure.attachment_type.TEXT,
            )
            allure.attach(
                response.headers.get("content-disposition", ""),
                "content_disposition",
                allure.attachment_type.TEXT,
            )
            assert response.content[:2] == b"PK", (
                f"200 OK but not XLSX (no PK). First bytes={response.content[:10]!r}"
            )
            return

    assert last is not None
    assert False, (
        f"Export failed: status={last.status_code}, url={last.url}, body={(last.text or '')[:HTTPStatus.OK]}"
    )
