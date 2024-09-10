import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    get_list_tasks_extended_endpoint = f'{HOST}/EXPORT/tasks/extended/includes'
    export_list_tasks_endpoint = f'{HOST}/EXPORT/tasks'
    export_list_tasks_extended_endpoint = f'{HOST}/EXPORT/tasks/extended'

    @staticmethod
    def export_list_extended_tasks_all_filters_by_task_id_endpoint(task_id: int) -> str:
        endpoint = (f'{HOST}/EXPORT/tasks/extended?taskID={task_id}&?include=LocationAddress&'
                    f'include=TaskActualityName&include=WorkTypeName&include=Completed&'
                    f'include=CompletedWorks&include=AssignedToUserDateTime&include=Requested&'
                    f'include=LocationLongitude&include=CompanyName&include=Closed&include=ScheduledStartDateTime&'
                    f'include=ScheduledFinishDateTime&include=AssignedToFullName&include=TaskStagingHistories&'
                    f'include=AssetClassName&include=ContactPerson&include=Deadline&include=CriticalityName&'
                    f'include=RequestMethodName&include=AssetDistrictsNames&include=FaultTimestamp&include=Number&'
                    f'include=AssetName&include=RequestedByFullName&include=CheckedIn&include=Notes&'
                    f'include=LocationDescription&include=ResponsibleFullName&include=EstimatedCost&'
                    f'include=EstimatedTimeConsumptionMinutes&include=ParentNumber&include=SerialNumber&'
                    f'include=Conversations&include=TaskStageName&include=TaskStatusName&'
                    f'include=LocationCountryName&include=ContactPhone&include=TaskTypeName&'
                    f'include=AssetTypeName&include=ActualCost&include=ActualTimeConsumptionMinutes&'
                    f'include=LocationTimezoneName&include=CheckListResults&include=LocationLatitude&'
                    f'include=ContactEmail&isClosed=false&isDeleted=false&isInitial=false&orderBy=1&'
                    f'searchText=&sortDirection=2')
        return endpoint
