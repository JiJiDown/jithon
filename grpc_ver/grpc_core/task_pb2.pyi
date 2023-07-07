from google.protobuf import empty_pb2 as _empty_pb2
from type import api_pb2 as _api_pb2
from type import video_pb2 as _video_pb2
from type import taskstatus_pb2 as _taskstatus_pb2
from type import taskdo_pb2 as _taskdo_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TaskNewReq(_message.Message):
    __slots__ = ["aid", "bvid", "cid", "video_quality", "audio_quality", "video_codec", "api_type", "save_filename", "audio_only"]
    AID_FIELD_NUMBER: _ClassVar[int]
    BVID_FIELD_NUMBER: _ClassVar[int]
    CID_FIELD_NUMBER: _ClassVar[int]
    VIDEO_QUALITY_FIELD_NUMBER: _ClassVar[int]
    AUDIO_QUALITY_FIELD_NUMBER: _ClassVar[int]
    VIDEO_CODEC_FIELD_NUMBER: _ClassVar[int]
    API_TYPE_FIELD_NUMBER: _ClassVar[int]
    SAVE_FILENAME_FIELD_NUMBER: _ClassVar[int]
    AUDIO_ONLY_FIELD_NUMBER: _ClassVar[int]
    aid: int
    bvid: str
    cid: int
    video_quality: int
    audio_quality: int
    video_codec: _video_pb2.VideoType
    api_type: _api_pb2.ApiType
    save_filename: str
    audio_only: bool
    def __init__(self, aid: _Optional[int] = ..., bvid: _Optional[str] = ..., cid: _Optional[int] = ..., video_quality: _Optional[int] = ..., audio_quality: _Optional[int] = ..., video_codec: _Optional[_Union[_video_pb2.VideoType, str]] = ..., api_type: _Optional[_Union[_api_pb2.ApiType, str]] = ..., save_filename: _Optional[str] = ..., audio_only: bool = ...) -> None: ...

class TaskNewReply(_message.Message):
    __slots__ = ["task_id", "quality_video", "quality_audio"]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    QUALITY_VIDEO_FIELD_NUMBER: _ClassVar[int]
    QUALITY_AUDIO_FIELD_NUMBER: _ClassVar[int]
    task_id: str
    quality_video: int
    quality_audio: int
    def __init__(self, task_id: _Optional[str] = ..., quality_video: _Optional[int] = ..., quality_audio: _Optional[int] = ...) -> None: ...

class TaskStatusReq(_message.Message):
    __slots__ = ["task_id"]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    task_id: str
    def __init__(self, task_id: _Optional[str] = ...) -> None: ...

class TaskStatusReply(_message.Message):
    __slots__ = ["task_status", "text", "progress", "average_speed"]
    TASK_STATUS_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    AVERAGE_SPEED_FIELD_NUMBER: _ClassVar[int]
    task_status: _taskstatus_pb2.TaskStatusType
    text: str
    progress: int
    average_speed: str
    def __init__(self, task_status: _Optional[_Union[_taskstatus_pb2.TaskStatusType, str]] = ..., text: _Optional[str] = ..., progress: _Optional[int] = ..., average_speed: _Optional[str] = ...) -> None: ...

class TaskControlReq(_message.Message):
    __slots__ = ["task_id", "do"]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    DO_FIELD_NUMBER: _ClassVar[int]
    task_id: str
    do: _taskdo_pb2.TaskDo
    def __init__(self, task_id: _Optional[str] = ..., do: _Optional[_Union[_taskdo_pb2.TaskDo, str]] = ...) -> None: ...
