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
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.PARTIAL_CONTENT, \
            f'Expected status code {HTTPStatus.PARTIAL_CONTENT}, but got {response.status_code}, {data_response}'
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
        Переходы по жизненному циклу заявки. Счетчик не больше 20 попыток поиска.
        """
        paths = []  # Список для хранения всех найденных путей
        queue = deque([(start_task_stage_id, [start_task_stage_id])])
        work_task_history_api = WorkTaskStagingHistoryAPI()
        visited_paths = set()  # Уникальные пути, чтобы избежать дублирования
        counts = 0
        last_valid_path = []  # Сохраняем последний путь, даже если он не доходит до конца

        while queue:
            if counts >= 20:
                logger.error('Searching all possible paths from the initial stage to the final stage is not found.')
                if last_valid_path:  # Если путь есть, добавляем его в `paths`
                    paths.append(last_valid_path)
                break

            current_stage, path = queue.popleft()
            counts += 1

            last_valid_path = path  # Обновляем последний найденный путь

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

                    # Проверка на зацикливание и дублирование пути
                    new_path = tuple(path + [to_stage_id])  # Делаем путь неизменяемым для хранения в `set`
                    if to_stage_id == start_task_stage_id or new_path in visited_paths:
                        continue

                    visited_paths.add(new_path)  # Запоминаем пройденный путь
                    queue.append((to_stage_id, list(new_path)))  # Добавляем в очередь

        logger.info(f'Found paths: {paths}')

        # Используем последний валидный путь, если ни один путь не дошёл до конца
        if not paths and last_valid_path:
            last_valid_path.append(finish_task_stage_id)
            paths.append(last_valid_path)

        if paths:
            for task_stage_id in paths[0][1:]:
                work_task_history_api.post_add_task_staging_history(
                    stage_id=str(task_stage_id),
                    task_id=task_id
                )

        return paths
