import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.tstg.tstg_task_stage_links.payloads import Payloads
from services.tstg.tstg_task_stage_links.endpoints import Endpoints
from config.headers import Headers
from services.tstg.tstg_task_stage_links.models.tstg_task_stage_links_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os
from collections import deque
from services.work.work_task_staging_history.api_work_task_staging_history import WorkTaskStagingHistoryAPI


load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class TstgTaskStageLinksAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Get list task stage links in tenant.")
    def get_list_task_stage_links_in_tenant(self, task_type_id: int, task_stage_from_id: int):
        params = {
            "taskTypeID": task_type_id,
            "taskStageFromID": task_stage_from_id
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_task_stage_links_endpoint, params=params,
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            f'Status code {response.status_code}, {response.json()}'
        model = SuccessGetListTaskStageLinksModel(links=response.json())
        logger.info(f'Successfully get list task stage links in tenant.')
        return model

    @allure.step("Get the path of task stage history from start to final and switch by task stages.")
    def get_list_task_stage_path_switch_from_start_to_finish(
            self,
            task_type_id: int,
            start_task_stage_id: int,
            finish_task_stage_id: int,
            task_id: int
    ):
        """
        Поиск всех возможных путей от начальной стадии к конечной, избегая циклов.
        Возвращает список списков ID стадий для каждого найденного пути.
        Переходы по жизненному циклу заявки.
        """
        paths = []  # Список для хранения всех найденных путей
        queue = deque([(start_task_stage_id, [start_task_stage_id])])
        work_task_history_api = WorkTaskStagingHistoryAPI()

        while queue:
            current_stage, path = queue.popleft()

            # Проверка, достигли ли мы конечной стадии
            if current_stage == finish_task_stage_id:
                paths.append(path)
                continue

            # Получаем переходы для текущей стадии
            stage_links_model = self.get_list_task_stage_links_in_tenant(
                task_type_id=task_type_id,
                task_stage_from_id=current_stage
            )

            for link in stage_links_model.links:
                if link.toTaskStage and link.toTaskStage.id:
                    to_stage_id = link.toTaskStage.id
                    # Проверка на циклы и возврат на начальную стадию
                    if to_stage_id == start_task_stage_id or to_stage_id in path:
                        continue

                    # Формируем новый путь с добавленной следующей стадией
                    new_path = path + [to_stage_id]

                    # Добавляем новый путь в очередь для дальнейшей обработки
                    queue.append((to_stage_id, new_path))
        list_path_type_stage_id = paths[0][1:]
        for task_stage_id in list_path_type_stage_id:
            work_task_history_api.post_add_task_staging_history(
                stage_id=str(task_stage_id),
                task_id=task_id
            )

        return paths
