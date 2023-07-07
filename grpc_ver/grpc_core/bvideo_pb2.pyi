from type import video_pb2 as _video_pb2
from type import api_pb2 as _api_pb2
from type import blinkresult_pb2 as _blinkresult_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BvideoContentReq(_message.Message):
    __slots__ = ["content"]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    content: str
    def __init__(self, content: _Optional[str] = ...) -> None: ...

class BvideoCheckContentReply(_message.Message):
    __slots__ = ["is_valid", "blink_result"]
    IS_VALID_FIELD_NUMBER: _ClassVar[int]
    BLINK_RESULT_FIELD_NUMBER: _ClassVar[int]
    is_valid: bool
    blink_result: _blinkresult_pb2.BLinkResult
    def __init__(self, is_valid: bool = ..., blink_result: _Optional[_Union[_blinkresult_pb2.BLinkResult, _Mapping]] = ...) -> None: ...

class BvideoInfoReply(_message.Message):
    __slots__ = ["blink_result", "video_cover", "video_title", "video_filename", "video_desc", "sub_sort", "sort", "up_name", "up_mid", "up_face", "bili_pubdate_str", "is_stein_gate", "block"]
    BLINK_RESULT_FIELD_NUMBER: _ClassVar[int]
    VIDEO_COVER_FIELD_NUMBER: _ClassVar[int]
    VIDEO_TITLE_FIELD_NUMBER: _ClassVar[int]
    VIDEO_FILENAME_FIELD_NUMBER: _ClassVar[int]
    VIDEO_DESC_FIELD_NUMBER: _ClassVar[int]
    SUB_SORT_FIELD_NUMBER: _ClassVar[int]
    SORT_FIELD_NUMBER: _ClassVar[int]
    UP_NAME_FIELD_NUMBER: _ClassVar[int]
    UP_MID_FIELD_NUMBER: _ClassVar[int]
    UP_FACE_FIELD_NUMBER: _ClassVar[int]
    BILI_PUBDATE_STR_FIELD_NUMBER: _ClassVar[int]
    IS_STEIN_GATE_FIELD_NUMBER: _ClassVar[int]
    BLOCK_FIELD_NUMBER: _ClassVar[int]
    blink_result: _blinkresult_pb2.BLinkResult
    video_cover: bytes
    video_title: str
    video_filename: str
    video_desc: str
    sub_sort: str
    sort: str
    up_name: str
    up_mid: int
    up_face: bytes
    bili_pubdate_str: str
    is_stein_gate: bool
    block: _containers.RepeatedCompositeFieldContainer[BvideoBlock]
    def __init__(self, blink_result: _Optional[_Union[_blinkresult_pb2.BLinkResult, _Mapping]] = ..., video_cover: _Optional[bytes] = ..., video_title: _Optional[str] = ..., video_filename: _Optional[str] = ..., video_desc: _Optional[str] = ..., sub_sort: _Optional[str] = ..., sort: _Optional[str] = ..., up_name: _Optional[str] = ..., up_mid: _Optional[int] = ..., up_face: _Optional[bytes] = ..., bili_pubdate_str: _Optional[str] = ..., is_stein_gate: bool = ..., block: _Optional[_Iterable[_Union[BvideoBlock, _Mapping]]] = ...) -> None: ...

class BvideoBlock(_message.Message):
    __slots__ = ["block_title", "list"]
    BLOCK_TITLE_FIELD_NUMBER: _ClassVar[int]
    LIST_FIELD_NUMBER: _ClassVar[int]
    block_title: str
    list: _containers.RepeatedCompositeFieldContainer[BvideoPage]
    def __init__(self, block_title: _Optional[str] = ..., list: _Optional[_Iterable[_Union[BvideoPage, _Mapping]]] = ...) -> None: ...

class BvideoPage(_message.Message):
    __slots__ = ["page_av", "page_bv", "page_cid", "page_index", "page_cover", "page_title", "page_info"]
    PAGE_AV_FIELD_NUMBER: _ClassVar[int]
    PAGE_BV_FIELD_NUMBER: _ClassVar[int]
    PAGE_CID_FIELD_NUMBER: _ClassVar[int]
    PAGE_INDEX_FIELD_NUMBER: _ClassVar[int]
    PAGE_COVER_FIELD_NUMBER: _ClassVar[int]
    PAGE_TITLE_FIELD_NUMBER: _ClassVar[int]
    PAGE_INFO_FIELD_NUMBER: _ClassVar[int]
    page_av: int
    page_bv: str
    page_cid: int
    page_index: int
    page_cover: bytes
    page_title: str
    page_info: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, page_av: _Optional[int] = ..., page_bv: _Optional[str] = ..., page_cid: _Optional[int] = ..., page_index: _Optional[int] = ..., page_cover: _Optional[bytes] = ..., page_title: _Optional[str] = ..., page_info: _Optional[_Iterable[str]] = ...) -> None: ...

class BvideoAllQualityReq(_message.Message):
    __slots__ = ["aid", "bvid", "cid"]
    AID_FIELD_NUMBER: _ClassVar[int]
    BVID_FIELD_NUMBER: _ClassVar[int]
    CID_FIELD_NUMBER: _ClassVar[int]
    aid: int
    bvid: str
    cid: int
    def __init__(self, aid: _Optional[int] = ..., bvid: _Optional[str] = ..., cid: _Optional[int] = ...) -> None: ...

class BvideoBVideoItem(_message.Message):
    __slots__ = ["quality_id", "quality_text", "codec", "frame_rate", "bit_rate", "stream_size", "api_type"]
    QUALITY_ID_FIELD_NUMBER: _ClassVar[int]
    QUALITY_TEXT_FIELD_NUMBER: _ClassVar[int]
    CODEC_FIELD_NUMBER: _ClassVar[int]
    FRAME_RATE_FIELD_NUMBER: _ClassVar[int]
    BIT_RATE_FIELD_NUMBER: _ClassVar[int]
    STREAM_SIZE_FIELD_NUMBER: _ClassVar[int]
    API_TYPE_FIELD_NUMBER: _ClassVar[int]
    quality_id: int
    quality_text: str
    codec: _video_pb2.VideoType
    frame_rate: str
    bit_rate: str
    stream_size: str
    api_type: _api_pb2.ApiType
    def __init__(self, quality_id: _Optional[int] = ..., quality_text: _Optional[str] = ..., codec: _Optional[_Union[_video_pb2.VideoType, str]] = ..., frame_rate: _Optional[str] = ..., bit_rate: _Optional[str] = ..., stream_size: _Optional[str] = ..., api_type: _Optional[_Union[_api_pb2.ApiType, str]] = ...) -> None: ...

class BvideoBAudioItem(_message.Message):
    __slots__ = ["quality_id", "quality_text", "codec_text", "bit_rate", "stream_size", "api_type"]
    QUALITY_ID_FIELD_NUMBER: _ClassVar[int]
    QUALITY_TEXT_FIELD_NUMBER: _ClassVar[int]
    CODEC_TEXT_FIELD_NUMBER: _ClassVar[int]
    BIT_RATE_FIELD_NUMBER: _ClassVar[int]
    STREAM_SIZE_FIELD_NUMBER: _ClassVar[int]
    API_TYPE_FIELD_NUMBER: _ClassVar[int]
    quality_id: int
    quality_text: str
    codec_text: str
    bit_rate: str
    stream_size: str
    api_type: _api_pb2.ApiType
    def __init__(self, quality_id: _Optional[int] = ..., quality_text: _Optional[str] = ..., codec_text: _Optional[str] = ..., bit_rate: _Optional[str] = ..., stream_size: _Optional[str] = ..., api_type: _Optional[_Union[_api_pb2.ApiType, str]] = ...) -> None: ...

class BvideoAllQualityReply(_message.Message):
    __slots__ = ["video", "audio"]
    VIDEO_FIELD_NUMBER: _ClassVar[int]
    AUDIO_FIELD_NUMBER: _ClassVar[int]
    video: _containers.RepeatedCompositeFieldContainer[BvideoBVideoItem]
    audio: _containers.RepeatedCompositeFieldContainer[BvideoBAudioItem]
    def __init__(self, video: _Optional[_Iterable[_Union[BvideoBVideoItem, _Mapping]]] = ..., audio: _Optional[_Iterable[_Union[BvideoBAudioItem, _Mapping]]] = ...) -> None: ...
