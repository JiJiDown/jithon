from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class VideoType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    VideoType_UNKNOWN: _ClassVar[VideoType]
    VideoType_AVC: _ClassVar[VideoType]
    VideoType_HEVC: _ClassVar[VideoType]
    VideoType_AV1: _ClassVar[VideoType]
VideoType_UNKNOWN: VideoType
VideoType_AVC: VideoType
VideoType_HEVC: VideoType
VideoType_AV1: VideoType
