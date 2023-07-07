from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class UpdateStatusType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    CHECKING: _ClassVar[UpdateStatusType]
    NOTSUPPORTUPDATE: _ClassVar[UpdateStatusType]
    UPTODATE: _ClassVar[UpdateStatusType]
    NEEDUPDATE: _ClassVar[UpdateStatusType]
CHECKING: UpdateStatusType
NOTSUPPORTUPDATE: UpdateStatusType
UPTODATE: UpdateStatusType
NEEDUPDATE: UpdateStatusType
