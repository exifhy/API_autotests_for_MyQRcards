import pprint

LIST_OF_TASK_EXPORT_FIELDS = [
    {
        "code": "LocationAddress",
        "description": "Адрес"
    },
    {
        "code": "TaskActualityName",
        "description": "Актуальность"
    },
    {
        "code": "WorkTypeName",
        "description": "Вид работ"
    },
    {
        "code": "Completed",
        "description": "Выполнена"
    },
    {
        "code": "CompletedWorks",
        "description": "Выполненные работы"
    },
    {
        "code": "AssignedToUserDateTime",
        "description": "Дата назначения"
    },
    {
        "code": "Requested",
        "description": "Дата создания"
    },
    {
        "code": "LocationLongitude",
        "description": "Долгота"
    },
    {
        "code": "CompanyName",
        "description": "Заказчик"
    },
    {
        "code": "Closed",
        "description": "Закрыта"
    },
    {
        "code": "AssignedToFullNames",
        "description": "Исполнитель"
    },
    {
        "code": "TaskStagingHistories",
        "description": "История перемещений по стадиям"
    },
    {
        "code": "AssetClassName",
        "description": "Класс объекта"
    },
    {
        "code": "ContactPerson",
        "description": "Контактное лицо"
    },
    {
        "code": "Deadline",
        "description": "Крайний срок закрытия"
    },
    {
        "code": "CriticalityName",
        "description": "Критичность"
    },
    {
        "code": "RequestMethodName",
        "description": "Метод подачи заявки"
    },
    {
        "code": "AssetDistrictsNames",
        "description": "Название участка"
    },
    {
        "code": "ScheduledFinishDateTime",
        "description": "Назначено По"
    },
    {
        "code": "ScheduledStartDateTime",
        "description": "Назначено С"
    },
    {
        "code": "FaultTimestamp",
        "description": "Неисправность обнаружена"
    },
    {
        "code": "Number",
        "description": "Номер"
    },
    {
        "code": "AssetName",
        "description": "Оборудование"
    },
    {
        "code": "RequestedByFullName",
        "description": "Обращение от"
    },
    {
        "code": "CheckedIn",
        "description": "Объект посещен"
    },
    {
        "code": "Notes",
        "description": "Описание заявки"
    },
    {
        "code": "LocationDescription",
        "description": "Описание объекта"
    },
    {
        "code": "ResponsibleFullName",
        "description": "Ответственный за объект"
    },
    {
        "code": "EstimatedCost",
        "description": "Оценочная стоимость"
    },
    {
        "code": "EstimatedTimeConsumptionMinutes",
        "description": "Оценочные трудозатраты"
    },
    {
        "code": "ParentNumber",
        "description": "Родительская заявка"
    },
    {
        "code": "SerialNumber",
        "description": "Серийный номер объекта"
    },
    {
        "code": "Conversations",
        "description": "Сообщения"
    },
    {
        "code": "TaskStageName",
        "description": "Стадия"
    },
    {
        "code": "TaskStatusName",
        "description": "Статус"
    },
    {
        "code": "LocationCountryName",
        "description": "Страна"
    },
    {
        "code": "ContactPhone",
        "description": "Телефон"
    },
    {
        "code": "TaskTypeName",
        "description": "Тип заявки"
    },
    {
        "code": "AssetTypeName",
        "description": "Тип объекта"
    },
    {
        "code": "ActualCost",
        "description": "Фактическая стоимость"
    },
    {
        "code": "ActualTimeConsumptionMinutes",
        "description": "Фактические трудозатраты"
    },
    {
        "code": "LocationTimezoneName",
        "description": "Часовой пояс"
    },
    {
        "code": "CheckListResults",
        "description": "Чек листы"
    },
    {
        "code": "000002",
        "description": "Шаблоны "
    },
    {
        "code": "LocationLatitude",
        "description": "Широта"
    },
    {
        "code": "ContactEmail",
        "description": "Электронная почта"
    }
]
