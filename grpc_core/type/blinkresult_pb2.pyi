from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class BLinkResult(_message.Message):
    __slots__ = ["id", "mark", "web_link"]
    ID_FIELD_NUMBER: _ClassVar[int]
    MARK_FIELD_NUMBER: _ClassVar[int]
    WEB_LINK_FIELD_NUMBER: _ClassVar[int]
    id: int
    mark: str
    web_link: str
    def __init__(self, id: _Optional[int] = ..., mark: _Optional[str] = ..., web_link: _Optional[str] = ...) -> None: ...
