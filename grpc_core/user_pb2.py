# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: user.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nuser.proto\x12\rjijidown.core\x1a\x1bgoogle/protobuf/empty.proto\"\x86\x01\n\rUserInfoReply\x12\x10\n\x08is_login\x18\x01 \x01(\x08\x12\x0b\n\x03mid\x18\x02 \x01(\x03\x12\r\n\x05uname\x18\x03 \x01(\t\x12\x0c\n\x04\x66\x61\x63\x65\x18\x04 \x01(\x0c\x12\x12\n\nvip_status\x18\x05 \x01(\x08\x12\x16\n\x0evip_label_text\x18\x06 \x01(\t\x12\r\n\x05\x62\x61\x64ge\x18\x07 \x01(\t\"@\n\x12UserLoginQRCodeReq\x12*\n\x03\x61pi\x18\x01 \x01(\x0e\x32\x1d.jijidown.core.LoginQRCodeAPI\"3\n\x14UserLoginQRCodeReply\x12\x0f\n\x07qr_code\x18\x01 \x01(\x0c\x12\n\n\x02id\x18\x02 \x01(\t\" \n\x12UserLoginStatusReq\x12\n\n\x02id\x18\x01 \x01(\t\"\\\n\x14UserLoginStatusReply\x12\x18\n\x10login_successful\x18\x01 \x01(\x08\x12*\n\x06status\x18\x02 \x01(\x0e\x32\x1a.jijidown.core.LoginStatus\"<\n\x13UserImportCookieReq\x12\x0f\n\x07\x63ookies\x18\x01 \x01(\t\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x02 \x01(\t*?\n\x0eLoginQRCodeAPI\x12\x16\n\x12LoginQRCodeAPI_WEB\x10\x00\x12\x15\n\x11LoginQRCodeAPI_TV\x10\x01*\x92\x01\n\x0bLoginStatus\x12\x17\n\x13LoginStatus_UNKNOWN\x10\x00\x12\x19\n\x15LoginStatus_SUCCEEDED\x10\x01\x12\x17\n\x13LoginStatus_EXPIRED\x10\x02\x12\x19\n\x15LoginStatus_UNSCANNED\x10\x03\x12\x1b\n\x17LoginStatus_UNCONFIRMED\x10\x04\x32\xc0\x02\n\x04User\x12<\n\x04Info\x12\x16.google.protobuf.Empty\x1a\x1c.jijidown.core.UserInfoReply\x12U\n\x0bLoginQRCode\x12!.jijidown.core.UserLoginQRCodeReq\x1a#.jijidown.core.UserLoginQRCodeReply\x12W\n\x0bLoginStatus\x12!.jijidown.core.UserLoginStatusReq\x1a#.jijidown.core.UserLoginStatusReply0\x01\x12J\n\x0cImportCookie\x12\".jijidown.core.UserImportCookieReq\x1a\x16.google.protobuf.EmptyBIZ3github.com/JiJiDown/JiJiDownCore-go/common/jijidown\xaa\x02\x11JiJiDown.Core.SDKb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'user_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z3github.com/JiJiDown/JiJiDownCore-go/common/jijidown\252\002\021JiJiDown.Core.SDK'
  _globals['_LOGINQRCODEAPI']._serialized_start=504
  _globals['_LOGINQRCODEAPI']._serialized_end=567
  _globals['_LOGINSTATUS']._serialized_start=570
  _globals['_LOGINSTATUS']._serialized_end=716
  _globals['_USERINFOREPLY']._serialized_start=59
  _globals['_USERINFOREPLY']._serialized_end=193
  _globals['_USERLOGINQRCODEREQ']._serialized_start=195
  _globals['_USERLOGINQRCODEREQ']._serialized_end=259
  _globals['_USERLOGINQRCODEREPLY']._serialized_start=261
  _globals['_USERLOGINQRCODEREPLY']._serialized_end=312
  _globals['_USERLOGINSTATUSREQ']._serialized_start=314
  _globals['_USERLOGINSTATUSREQ']._serialized_end=346
  _globals['_USERLOGINSTATUSREPLY']._serialized_start=348
  _globals['_USERLOGINSTATUSREPLY']._serialized_end=440
  _globals['_USERIMPORTCOOKIEREQ']._serialized_start=442
  _globals['_USERIMPORTCOOKIEREQ']._serialized_end=502
  _globals['_USER']._serialized_start=719
  _globals['_USER']._serialized_end=1039
# @@protoc_insertion_point(module_scope)
