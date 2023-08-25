from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LoginQRCodeAPI(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    LoginQRCodeAPI_WEB: _ClassVar[LoginQRCodeAPI]
    LoginQRCodeAPI_TV: _ClassVar[LoginQRCodeAPI]

class LoginStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    LoginStatus_UNKNOWN: _ClassVar[LoginStatus]
    LoginStatus_SUCCEEDED: _ClassVar[LoginStatus]
    LoginStatus_EXPIRED: _ClassVar[LoginStatus]
    LoginStatus_UNSCANNED: _ClassVar[LoginStatus]
    LoginStatus_UNCONFIRMED: _ClassVar[LoginStatus]
LoginQRCodeAPI_WEB: LoginQRCodeAPI
LoginQRCodeAPI_TV: LoginQRCodeAPI
LoginStatus_UNKNOWN: LoginStatus
LoginStatus_SUCCEEDED: LoginStatus
LoginStatus_EXPIRED: LoginStatus
LoginStatus_UNSCANNED: LoginStatus
LoginStatus_UNCONFIRMED: LoginStatus

class UserInfoReply(_message.Message):
    __slots__ = ["is_login", "mid", "uname", "face", "vip_status", "vip_label_text", "badge"]
    IS_LOGIN_FIELD_NUMBER: _ClassVar[int]
    MID_FIELD_NUMBER: _ClassVar[int]
    UNAME_FIELD_NUMBER: _ClassVar[int]
    FACE_FIELD_NUMBER: _ClassVar[int]
    VIP_STATUS_FIELD_NUMBER: _ClassVar[int]
    VIP_LABEL_TEXT_FIELD_NUMBER: _ClassVar[int]
    BADGE_FIELD_NUMBER: _ClassVar[int]
    is_login: bool
    mid: int
    uname: str
    face: bytes
    vip_status: bool
    vip_label_text: str
    badge: str
    def __init__(self, is_login: bool = ..., mid: _Optional[int] = ..., uname: _Optional[str] = ..., face: _Optional[bytes] = ..., vip_status: bool = ..., vip_label_text: _Optional[str] = ..., badge: _Optional[str] = ...) -> None: ...

class UserLoginQRCodeReq(_message.Message):
    __slots__ = ["api"]
    API_FIELD_NUMBER: _ClassVar[int]
    api: LoginQRCodeAPI
    def __init__(self, api: _Optional[_Union[LoginQRCodeAPI, str]] = ...) -> None: ...

class UserLoginQRCodeReply(_message.Message):
    __slots__ = ["qr_code", "id"]
    QR_CODE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    qr_code: bytes
    id: str
    def __init__(self, qr_code: _Optional[bytes] = ..., id: _Optional[str] = ...) -> None: ...

class UserLoginStatusReq(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class UserLoginStatusReply(_message.Message):
    __slots__ = ["login_successful", "status"]
    LOGIN_SUCCESSFUL_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    login_successful: bool
    status: LoginStatus
    def __init__(self, login_successful: bool = ..., status: _Optional[_Union[LoginStatus, str]] = ...) -> None: ...

class UserImportCookieReq(_message.Message):
    __slots__ = ["cookies", "access_token"]
    COOKIES_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    cookies: str
    access_token: str
    def __init__(self, cookies: _Optional[str] = ..., access_token: _Optional[str] = ...) -> None: ...
