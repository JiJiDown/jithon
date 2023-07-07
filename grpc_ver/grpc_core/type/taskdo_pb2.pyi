from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class TaskDo(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    TaskDo_NOTHING: _ClassVar[TaskDo]
    TaskDo_PAUSE: _ClassVar[TaskDo]
    TaskDo_RESUME: _ClassVar[TaskDo]
    TaskDo_DELETE: _ClassVar[TaskDo]
    TaskDo_DELETE_AND_FILE: _ClassVar[TaskDo]
TaskDo_NOTHING: TaskDo
TaskDo_PAUSE: TaskDo
TaskDo_RESUME: TaskDo
TaskDo_DELETE: TaskDo
TaskDo_DELETE_AND_FILE: TaskDo
