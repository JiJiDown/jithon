from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class ApiType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    ApiType_WEB: _ClassVar[ApiType]
    ApiType_TV: _ClassVar[ApiType]
    ApiType_APP: _ClassVar[ApiType]
ApiType_WEB: ApiType
ApiType_TV: ApiType
ApiType_APP: ApiType
