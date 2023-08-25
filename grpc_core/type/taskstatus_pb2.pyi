from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class TaskStatusType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    TaskStatusType_TASK_ERROR: _ClassVar[TaskStatusType]
    TaskStatusType_TASK_PAUSE: _ClassVar[TaskStatusType]
    TaskStatusType_TASK_RUNNING: _ClassVar[TaskStatusType]
    TaskStatusType_TASK_WAIT: _ClassVar[TaskStatusType]
    TaskStatusType_TASK_MERGEING: _ClassVar[TaskStatusType]
    TaskStatusType_TASK_GENMUSIC: _ClassVar[TaskStatusType]
    TaskStatusType_TASK_COMPLETE: _ClassVar[TaskStatusType]
TaskStatusType_TASK_ERROR: TaskStatusType
TaskStatusType_TASK_PAUSE: TaskStatusType
TaskStatusType_TASK_RUNNING: TaskStatusType
TaskStatusType_TASK_WAIT: TaskStatusType
TaskStatusType_TASK_MERGEING: TaskStatusType
TaskStatusType_TASK_GENMUSIC: TaskStatusType
TaskStatusType_TASK_COMPLETE: TaskStatusType
