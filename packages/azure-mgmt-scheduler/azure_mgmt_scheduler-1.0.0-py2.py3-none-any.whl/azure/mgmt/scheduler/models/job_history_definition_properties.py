# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class JobHistoryDefinitionProperties(Model):
    """JobHistoryDefinitionProperties.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar start_time: Gets the start time for this job.
    :vartype start_time: datetime
    :ivar end_time: Gets the end time for this job.
    :vartype end_time: datetime
    :ivar expected_execution_time: Gets the expected execution time for this
     job.
    :vartype expected_execution_time: datetime
    :ivar action_name: Gets the job history action name. Possible values
     include: 'MainAction', 'ErrorAction'
    :vartype action_name: str or :class:`JobHistoryActionName
     <azure.mgmt.scheduler.models.JobHistoryActionName>`
    :ivar status: Gets the job history status. Possible values include:
     'Completed', 'Failed', 'Postponed'
    :vartype status: str or :class:`JobExecutionStatus
     <azure.mgmt.scheduler.models.JobExecutionStatus>`
    :ivar message: Gets the message for the job history.
    :vartype message: str
    :ivar retry_count: Gets the retry count for job.
    :vartype retry_count: int
    :ivar repeat_count: Gets the repeat count for the job.
    :vartype repeat_count: int
    """ 

    _validation = {
        'start_time': {'readonly': True},
        'end_time': {'readonly': True},
        'expected_execution_time': {'readonly': True},
        'action_name': {'readonly': True},
        'status': {'readonly': True},
        'message': {'readonly': True},
        'retry_count': {'readonly': True},
        'repeat_count': {'readonly': True},
    }

    _attribute_map = {
        'start_time': {'key': 'startTime', 'type': 'iso-8601'},
        'end_time': {'key': 'endTime', 'type': 'iso-8601'},
        'expected_execution_time': {'key': 'expectedExecutionTime', 'type': 'iso-8601'},
        'action_name': {'key': 'actionName', 'type': 'JobHistoryActionName'},
        'status': {'key': 'status', 'type': 'JobExecutionStatus'},
        'message': {'key': 'message', 'type': 'str'},
        'retry_count': {'key': 'retryCount', 'type': 'int'},
        'repeat_count': {'key': 'repeatCount', 'type': 'int'},
    }

    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.expected_execution_time = None
        self.action_name = None
        self.status = None
        self.message = None
        self.retry_count = None
        self.repeat_count = None
