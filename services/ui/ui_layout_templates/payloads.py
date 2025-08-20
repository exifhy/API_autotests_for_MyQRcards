class Payloads:

    @staticmethod
    def post_add_layout_template_payload(default: bool, name: str, task_type_id: int or None) -> dict:
        payload = {
            "name": name,
            "IsDefault": default,
            "columns": [
                {
                    "index": 1,
                    "blocks": [
                        {
                            "index": 1,
                            "name": "Заявка",
                            "fields": [
                                {
                                    "index": 1,
                                    "label": "Номер заявки",
                                    "code": "number",
                                    "type": 1
                                },
                                {
                                    "index": 2,
                                    "label": "Тип заявки",
                                    "code": "taskTypeID",
                                    "type": 1
                                },
                                {
                                    "index": 3,
                                    "label": "Критичность",
                                    "code": "criticalityID",
                                    "type": 1
                                },
                                {
                                    "index": 4,
                                    "label": "Описание заявки",
                                    "code": "notes",
                                    "type": 1
                                },
                                {
                                    "index": 5,
                                    "label": "Добавить Исполнителя",
                                    "code": "assignedTo",
                                    "type": 1
                                },
                                {
                                    "index": 6,
                                    "label": "ИНН",
                                    "code": "inn",
                                    "type": 1
                                },
                                {
                                    "index": 7,
                                    "label": "Крайний срок закрытия",
                                    "code": "deadline",
                                    "type": 1
                                },
                                {
                                    "index": 8,
                                    "label": "Компания-Получатель платежа",
                                    "code": "payeeCompanyID",
                                    "type": 1
                                },
                                {
                                    "index": 9,
                                    "label": "Родительская заявка",
                                    "code": "parentID",
                                    "type": 1
                                },
                                {
                                    "index": 10,
                                    "label": "Поле загрузки файлов",
                                    "code": "attachments",
                                    "type": 1
                                },
                                {
                                    "index": 11,
                                    "label": "пользак",
                                    "code": "116",
                                    "type": 2
                                },
                                {
                                    "index": 12,
                                    "label": "Шаблоны ",
                                    "code": "2",
                                    "type": 2
                                },
                                {
                                    "index": 13,
                                    "label": "Правило расчета крайнего срока закрытия",
                                    "code": "deadlineRule",
                                    "type": 1
                                }
                            ]
                        },
                        {
                            "index": 2,
                            "name": "Трудозатраты",
                            "fields": [
                                {
                                    "index": 1,
                                    "label": "Оценочные трудозатраты",
                                    "code": "estimatedTimeConsumptionMinutes",
                                    "type": 1
                                },
                                {
                                    "index": 2,
                                    "label": "Оценочная стоимость",
                                    "code": "estimatedCost",
                                    "type": 1
                                },
                                {
                                    "index": 3,
                                    "label": "Фактические трудозатраты",
                                    "code": "actualTimeConsumptionMinutes",
                                    "type": 1
                                },
                                {
                                    "index": 4,
                                    "label": "Фактическая стоимость",
                                    "code": "actualCost",
                                    "type": 1
                                }
                            ]
                        }
                    ]
                },
                {
                    "index": 2,
                    "blocks": [
                        {
                            "index": 1,
                            "name": "Обслуживание заказчика",
                            "fields": [
                                {
                                    "index": 1,
                                    "label": "Компания-Заказчик",
                                    "code": "companyID",
                                    "type": 1
                                },
                                {
                                    "index": 2,
                                    "label": "Выбрать Объект",
                                    "code": "assetID",
                                    "type": 1
                                },
                                {
                                    "index": 3,
                                    "label": "Вид работ",
                                    "code": "workTypeID",
                                    "type": 1
                                },
                                {
                                    "index": 4,
                                    "label": "Договор обслуживания",
                                    "code": "contractID",
                                    "type": 1
                                },
                                {
                                    "index": 5,
                                    "label": "Выбрать адрес",
                                    "code": "locationID",
                                    "type": 1
                                },
                                {
                                    "index": 6,
                                    "label": "План объекта",
                                    "code": "assetSchema",
                                    "type": 1
                                },
                                {
                                    "index": 7,
                                    "label": "Компания-плательщик",
                                    "code": "payerCompanyID",
                                    "type": 1
                                },
                                {
                                    "index": 8,
                                    "label": "Добавить контактное лицо",
                                    "code": "contactPerson",
                                    "type": 1
                                },
                                {
                                    "index": 9,
                                    "label": "Контакты по заказчику и объектам",
                                    "code": "assetContacts",
                                    "type": 1
                                }
                            ]
                        },
                        {
                            "index": 2,
                            "name": "Детальная информация",
                            "fields": [
                                {
                                    "index": 1,
                                    "label": "Идентификатор ERPID",
                                    "code": "erpID",
                                    "type": 1
                                },
                                {
                                    "index": 2,
                                    "label": "Неисправность обнаружена",
                                    "code": "faultTimestamp",
                                    "type": 1
                                },
                                {
                                    "index": 3,
                                    "label": "Метод подачи заявки",
                                    "code": "requestMethodID",
                                    "type": 1
                                },
                                {
                                    "index": 4,
                                    "label": "Выбрать инициатора",
                                    "code": "requestedByUserID",
                                    "type": 1
                                }
                            ]
                        }
                    ]
                }
            ],
            "taskTypes": [] if task_type_id is None else [task_type_id]
        }
        return payload

    @staticmethod
    def post_add_layout_template_without_fields_payload(default: bool, name: str) -> dict:
        payload = {
            "name": name,
            "IsDefault": default,
            "columns": [
                {
                    "index": 1,
                    "blocks": []
                }
            ],
            "taskTypes": []
        }
        return payload

    @staticmethod
    def put_update_layout_template_payload(default: bool, name: str, task_type_id: int or None) -> dict:
        payload = {
            "name": name,
            "IsDefault": default,
            "columns": [
                {
                    "index": 1,
                    "blocks": [
                        {
                            "index": 1,
                            "name": "Заявка",
                            "fields": [
                                {
                                    "index": 1,
                                    "label": "Номер заявки",
                                    "code": "number",
                                    "type": 1
                                },
                                {
                                    "index": 2,
                                    "label": "Тип заявки",
                                    "code": "taskTypeID",
                                    "type": 1
                                },
                                {
                                    "index": 3,
                                    "label": "Критичность",
                                    "code": "criticalityID",
                                    "type": 1
                                },
                                {
                                    "index": 4,
                                    "label": "Описание заявки",
                                    "code": "notes",
                                    "type": 1
                                },
                                {
                                    "index": 5,
                                    "label": "Добавить Исполнителя",
                                    "code": "assignedTo",
                                    "type": 1
                                },
                                {
                                    "index": 6,
                                    "label": "ИНН",
                                    "code": "inn",
                                    "type": 1
                                },
                                {
                                    "index": 7,
                                    "label": "Крайний срок закрытия",
                                    "code": "deadline",
                                    "type": 1
                                },
                                {
                                    "index": 8,
                                    "label": "Компания-Получатель платежа",
                                    "code": "payeeCompanyID",
                                    "type": 1
                                },
                                {
                                    "index": 9,
                                    "label": "Родительская заявка",
                                    "code": "parentID",
                                    "type": 1
                                },
                                {
                                    "index": 10,
                                    "label": "Поле загрузки файлов",
                                    "code": "attachments",
                                    "type": 1
                                },
                                {
                                    "index": 11,
                                    "label": "пользак",
                                    "code": "116",
                                    "type": 2
                                },
                                {
                                    "index": 12,
                                    "label": "Шаблоны ",
                                    "code": "2",
                                    "type": 2
                                },
                                {
                                    "index": 13,
                                    "label": "Правило расчета крайнего срока закрытия",
                                    "code": "deadlineRule",
                                    "type": 1
                                }
                            ]
                        }
                    ]
                }
            ],
            "taskTypes": [] if task_type_id is None else [task_type_id]
        }
        return payload

    @staticmethod
    def put_add_task_types_to_layout_template_payload(*task_types_ids: int or tuple) -> list:
        return [*task_types_ids]

    @staticmethod
    def delete_task_types_from_layout_template_payload(*task_types_ids: int or tuple) -> list:
        return [*task_types_ids]
