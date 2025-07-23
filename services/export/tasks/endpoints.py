from config.config import HOST


class Endpoints:

    get_list_tasks_extended_endpoint = f'{HOST}/EXPORT/tasks/extended/includes'
    export_list_tasks_endpoint = f'{HOST}/EXPORT/tasks'
    export_list_tasks_v2_endpoint = f'{HOST}/EXPORT/tasks/v2.0'
    export_list_tasks_extended_endpoint = f'{HOST}/EXPORT/tasks/extended'
    export_empty_template_for_importing_task_endpoint = f'{HOST}/EXPORT/tasks/noData'

    @staticmethod
    def export_list_extended_tasks_all_filters_by_task_id_endpoint(number: str) -> str:
        endpoint = (f'{HOST}/EXPORT/tasks/extended?include=LocationAddress&'
                    f'include=TaskActualityName&include=WorkTypeName&'
                    f'include=Completed&include=CompletedWorks&'
                    f'include=AssignedToUserDateTime&include=Requested&'
                    f'include=LocationLongitude&include=CompanyName&'
                    f'include=Closed&include=AssignedToFullNames&'
                    f'include=TaskStagingHistories&include=AssetClassName&'
                    f'include=ContactPerson&include=Deadline&'
                    f'include=CriticalityName&include=RequestMethodName&'
                    f'include=AssetDistrictsNames&include=ScheduledFinishDateTime&'
                    f'include=ScheduledStartDateTime&include=FaultTimestamp&'
                    f'include=Number&include=AssetName&include=RequestedByFullName&'
                    f'include=CheckedIn&include=Notes&include=LocationDescription&'
                    f'include=ResponsibleFullName&include=EstimatedCost&'
                    f'include=EstimatedTimeConsumptionMinutes&include=ParentNumber&'
                    f'include=SerialNumber&include=Conversations&'
                    f'include=TaskStageName&include=TaskStatusName&'
                    f'include=LocationCountryName&include=ContactPhone&'
                    f'include=TaskTypeName&include=AssetTypeName&'
                    f'include=ActualCost&include=ActualTimeConsumptionMinutes&'
                    f'include=LocationTimezoneName&include=CheckListResults&'
                    f'include=000002&include=LocationLatitude&include=ContactEmail&'
                    f'ignoreConvertFilterParamsForNavigateMiddleware=true&'
                    f'isClosed=false&isDeleted=false&isInitial=false&orderBy=1&'
                    f'searchText={number}%20&sortDirection=2')
        return endpoint

    @staticmethod
    def export_list_extended_v2_tasks_all_filters_by_task_id_endpoint(number: str) -> str:
        endpoint = (f'{HOST}/EXPORT/tasks/extended/V2?include=LocationAddress&'
                    f'include=TaskActualityName&include=WorkTypeName&'
                    f'include=Completed&include=CompletedWorks&'
                    f'include=AssignedToUserDateTime&include=Requested&'
                    f'include=LocationLongitude&include=CompanyName&'
                    f'include=Closed&include=AssignedToFullNames&'
                    f'include=TaskStagingHistories&include=AssetClassName&'
                    f'include=ContactPerson&include=Deadline&'
                    f'include=CriticalityName&include=RequestMethodName&'
                    f'include=AssetDistrictsNames&include=ScheduledFinishDateTime&'
                    f'include=ScheduledStartDateTime&include=FaultTimestamp&'
                    f'include=Number&include=AssetName&include=RequestedByFullName&'
                    f'include=CheckedIn&include=Notes&include=LocationDescription&'
                    f'include=ResponsibleFullName&include=EstimatedCost&'
                    f'include=EstimatedTimeConsumptionMinutes&include=ParentNumber&'
                    f'include=SerialNumber&include=Conversations&'
                    f'include=TaskStageName&include=TaskStatusName&'
                    f'include=LocationCountryName&include=ContactPhone&'
                    f'include=TaskTypeName&include=AssetTypeName&'
                    f'include=ActualCost&include=ActualTimeConsumptionMinutes&'
                    f'include=LocationTimezoneName&include=CheckListResults&'
                    f'include=000002&include=LocationLatitude&include=ContactEmail&'
                    f'ignoreConvertFilterParamsForNavigateMiddleware=true&'
                    f'isClosed=false&isDeleted=false&isInitial=false&orderBy=1&'
                    f'searchText={number}%20&sortDirection=2')
        return endpoint
