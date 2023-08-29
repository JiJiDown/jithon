from google.protobuf import empty_pb2 as _empty_pb2
from type import api_pb2 as _api_pb2
from type import video_pb2 as _video_pb2
from type import taskstatus_pb2 as _taskstatus_pb2
from type import taskdo_pb2 as _taskdo_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TaskNewReq(_message.Message):
    __slots__ = ["aid", "bvid", "cid", "video_quality", "audio_quality", "video_codec", "api_type", "save_filename", "audio_only", "callback"]
    AID_FIELD_NUMBER: _ClassVar[int]
    BVID_FIELD_NUMBER: _ClassVar[int]
    CID_FIELD_NUMBER: _ClassVar[int]
    VIDEO_QUALITY_FIELD_NUMBER: _ClassVar[int]
    AUDIO_QUALITY_FIELD_NUMBER: _ClassVar[int]
    VIDEO_CODEC_FIELD_NUMBER: _ClassVar[int]
    API_TYPE_FIELD_NUMBER: _ClassVar[int]
    SAVE_FILENAME_FIELD_NUMBER: _ClassVar[int]
    AUDIO_ONLY_FIELD_NUMBER: _ClassVar[int]
    CALLBACK_FIELD_NUMBER: _ClassVar[int]
    aid: int
    bvid: str
    cid: int
    video_quality: int
    audio_quality: int
    video_codec: _video_pb2.VideoType
    api_type: _api_pb2.ApiType
    save_filename: str
    audio_only: bool
    callback: int
    def __init__(self, aid: _Optional[int] = ..., bvid: _Optional[str] = ..., cid: _Optional[int] = ..., video_quality: _Optional[int] = ..., audio_quality: _Optional[int] = ..., video_codec: _Optional[_Union[_video_pb2.VideoType, str]] = ..., api_type: _Optional[_Union[_api_pb2.ApiType, str]] = ..., save_filename: _Optional[str] = ..., audio_only: bool = ..., callback: _Optional[int] = ...) -> None: ...

class TaskCreationStatus(_message.Message):
    __slots__ = ["callback", "err"]
    CALLBACK_FIELD_NUMBER: _ClassVar[int]
    ERR_FIELD_NUMBER: _ClassVar[int]
    callback: int
    err: str
    def __init__(self, callback: _Optional[int] = ..., err: _Optional[str] = ...) -> None: ...

class TaskNewBatchReply(_message.Message):
    __slots__ = ["task_creation_status"]
    TASK_CREATION_STATUS_FIELD_NUMBER: _ClassVar[int]
    task_creation_status: _containers.RepeatedCompositeFieldContainer[TaskCreationStatus]
    def __init__(self, task_creation_status: _Optional[_Iterable[_Union[TaskCreationStatus, _Mapping]]] = ...) -> None: ...

class TaskNewBatchReq(_message.Message):
    __slots__ = ["new_tasks"]
    NEW_TASKS_FIELD_NUMBER: _ClassVar[int]
    new_tasks: _containers.RepeatedCompositeFieldContainer[TaskNewReq]
    def __init__(self, new_tasks: _Optional[_Iterable[_Union[TaskNewReq, _Mapping]]] = ...) -> None: ...

class TaskStatusReq(_message.Message):
    __slots__ = ["task_id"]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    task_id: str
    def __init__(self, task_id: _Optional[str] = ...) -> None: ...

class TaskProgress(_message.Message):
    __slots__ = ["total_length", "completed_length", "left_length", "download_speed", "eta", "progress"]
    TOTAL_LENGTH_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_LENGTH_FIELD_NUMBER: _ClassVar[int]
    LEFT_LENGTH_FIELD_NUMBER: _ClassVar[int]
    DOWNLOAD_SPEED_FIELD_NUMBER: _ClassVar[int]
    ETA_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    total_length: str
    completed_length: str
    left_length: str
    download_speed: str
    eta: str
    progress: int
    def __init__(self, total_length: _Optional[str] = ..., completed_length: _Optional[str] = ..., left_length: _Optional[str] = ..., download_speed: _Optional[str] = ..., eta: _Optional[str] = ..., progress: _Optional[int] = ...) -> None: ...

class TaskStatusReply(_message.Message):
    __slots__ = ["task_id", "task_title", "video_badge", "audio_badge", "video_codec", "api_type", "audio_only", "task_status", "add_time", "complete_time", "progress", "save_path"]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    TASK_TITLE_FIELD_NUMBER: _ClassVar[int]
    VIDEO_BADGE_FIELD_NUMBER: _ClassVar[int]
    AUDIO_BADGE_FIELD_NUMBER: _ClassVar[int]
    VIDEO_CODEC_FIELD_NUMBER: _ClassVar[int]
    API_TYPE_FIELD_NUMBER: _ClassVar[int]
    AUDIO_ONLY_FIELD_NUMBER: _ClassVar[int]
    TASK_STATUS_FIELD_NUMBER: _ClassVar[int]
    ADD_TIME_FIELD_NUMBER: _ClassVar[int]
    COMPLETE_TIME_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    SAVE_PATH_FIELD_NUMBER: _ClassVar[int]
    task_id: str
    task_title: str
    video_badge: str
    audio_badge: str
    video_codec: str
    api_type: _api_pb2.ApiType
    audio_only: bool
    task_status: _taskstatus_pb2.TaskStatusType
    add_time: int
    complete_time: int
    progress: TaskProgress
    save_path: str
    def __init__(self, task_id: _Optional[str] = ..., task_title: _Optional[str] = ..., video_badge: _Optional[str] = ..., audio_badge: _Optional[str] = ..., video_codec: _Optional[str] = ..., api_type: _Optional[_Union[_api_pb2.ApiType, str]] = ..., audio_only: bool = ..., task_status: _Optional[_Union[_taskstatus_pb2.TaskStatusType, str]] = ..., add_time: _Optional[int] = ..., complete_time: _Optional[int] = ..., progress: _Optional[_Union[TaskProgress, _Mapping]] = ..., save_path: _Optional[str] = ...) -> None: ...

class TaskListReq(_message.Message):
    __slots__ = ["task_status"]
    TASK_STATUS_FIELD_NUMBER: _ClassVar[int]
    task_status: _taskstatus_pb2.TaskStatusType
    def __init__(self, task_status: _Optional[_Union[_taskstatus_pb2.TaskStatusType, str]] = ...) -> None: ...

class TaskListReply(_message.Message):
    __slots__ = ["tasks"]
    TASKS_FIELD_NUMBER: _ClassVar[int]
    tasks: _containers.RepeatedCompositeFieldContainer[TaskStatusReply]
    def __init__(self, tasks: _Optional[_Iterable[_Union[TaskStatusReply, _Mapping]]] = ...) -> None: ...

class TaskControlReq(_message.Message):
    __slots__ = ["task_id", "do"]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    DO_FIELD_NUMBER: _ClassVar[int]
    task_id: str
    do: _taskdo_pb2.TaskDo
    def __init__(self, task_id: _Optional[str] = ..., do: _Optional[_Union[_taskdo_pb2.TaskDo, str]] = ...) -> None: ...

class TaskNotificationReply(_message.Message):
    __slots__ = ["task_id", "task_title", "average_speed", "elapsed_time"]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    TASK_TITLE_FIELD_NUMBER: _ClassVar[int]
    AVERAGE_SPEED_FIELD_NUMBER: _ClassVar[int]
    ELAPSED_TIME_FIELD_NUMBER: _ClassVar[int]
    task_id: str
    task_title: str
    average_speed: str
    elapsed_time: str
    def __init__(self, task_id: _Optional[str] = ..., task_title: _Optional[str] = ..., average_speed: _Optional[str] = ..., elapsed_time: _Optional[str] = ...) -> None: ...
