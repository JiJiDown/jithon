from google.protobuf import empty_pb2 as _empty_pb2
from type import servericon_pb2 as _servericon_pb2
from type import updatestatus_pb2 as _updatestatus_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StatusPingPong(_message.Message):
    __slots__ = ["server_name", "os_icon", "os_system_name"]
    SERVER_NAME_FIELD_NUMBER: _ClassVar[int]
    OS_ICON_FIELD_NUMBER: _ClassVar[int]
    OS_SYSTEM_NAME_FIELD_NUMBER: _ClassVar[int]
    server_name: str
    os_icon: _servericon_pb2.ServerIconType
    os_system_name: str
    def __init__(self, server_name: _Optional[str] = ..., os_icon: _Optional[_Union[_servericon_pb2.ServerIconType, str]] = ..., os_system_name: _Optional[str] = ...) -> None: ...

class StatusCheckUpdateReply(_message.Message):
    __slots__ = ["status", "change_log"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CHANGE_LOG_FIELD_NUMBER: _ClassVar[int]
    status: _updatestatus_pb2.UpdateStatusType
    change_log: str
    def __init__(self, status: _Optional[_Union[_updatestatus_pb2.UpdateStatusType, str]] = ..., change_log: _Optional[str] = ...) -> None: ...
