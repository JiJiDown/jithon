# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: bvideo.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from grpc_core.type import video_pb2 as type_dot_video__pb2
from grpc_core.type import api_pb2 as type_dot_api__pb2
from grpc_core.type import blinkresult_pb2 as type_dot_blinkresult__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0c\x62video.proto\x12\rjijidown.core\x1a\x10type/video.proto\x1a\x0etype/api.proto\x1a\x16type/blinkresult.proto\"#\n\x10\x42videoContentReq\x12\x0f\n\x07\x63ontent\x18\x01 \x01(\t\"]\n\x17\x42videoCheckContentReply\x12\x10\n\x08is_valid\x18\x01 \x01(\x08\x12\x30\n\x0c\x62link_result\x18\x02 \x01(\x0b\x32\x1a.jijidown.core.BLinkResult\"\xc7\x02\n\x0f\x42videoInfoReply\x12\x30\n\x0c\x62link_result\x18\x01 \x01(\x0b\x32\x1a.jijidown.core.BLinkResult\x12\x13\n\x0bvideo_cover\x18\x02 \x01(\x0c\x12\x13\n\x0bvideo_title\x18\x03 \x01(\t\x12\x16\n\x0evideo_filename\x18\x04 \x01(\t\x12\x12\n\nvideo_desc\x18\x05 \x01(\t\x12\x10\n\x08sub_sort\x18\x06 \x01(\t\x12\x0c\n\x04sort\x18\x07 \x01(\t\x12\x0f\n\x07up_name\x18\t \x01(\t\x12\x0e\n\x06up_mid\x18\n \x01(\x03\x12\x0f\n\x07up_face\x18\x0b \x01(\x0c\x12\x18\n\x10\x62ili_pubdate_str\x18\x0c \x01(\t\x12\x15\n\ris_stein_gate\x18\r \x01(\x08\x12)\n\x05\x62lock\x18\x0e \x03(\x0b\x32\x1a.jijidown.core.BvideoBlock\"K\n\x0b\x42videoBlock\x12\x13\n\x0b\x62lock_title\x18\x01 \x01(\t\x12\'\n\x04list\x18\x02 \x03(\x0b\x32\x19.jijidown.core.BvideoPage\"\x8f\x01\n\nBvideoPage\x12\x0f\n\x07page_av\x18\x01 \x01(\x03\x12\x0f\n\x07page_bv\x18\x02 \x01(\t\x12\x10\n\x08page_cid\x18\x03 \x01(\x03\x12\x12\n\npage_index\x18\x04 \x01(\x05\x12\x12\n\npage_cover\x18\x05 \x01(\x0c\x12\x12\n\npage_title\x18\x06 \x01(\t\x12\x11\n\tpage_info\x18\x07 \x03(\t\"=\n\x13\x42videoAllQualityReq\x12\x0b\n\x03\x61id\x18\x01 \x01(\x03\x12\x0c\n\x04\x62vid\x18\x02 \x01(\t\x12\x0b\n\x03\x63id\x18\x03 \x01(\x03\"\xca\x01\n\x10\x42videoBVideoItem\x12\x12\n\nquality_id\x18\x01 \x01(\r\x12\x14\n\x0cquality_text\x18\x02 \x01(\t\x12\'\n\x05\x63odec\x18\x03 \x01(\x0e\x32\x18.jijidown.core.VideoType\x12\x12\n\nframe_rate\x18\x04 \x01(\t\x12\x10\n\x08\x62it_rate\x18\x05 \x01(\t\x12\x13\n\x0bstream_size\x18\x06 \x01(\t\x12(\n\x08\x61pi_type\x18\x07 \x01(\x0e\x32\x16.jijidown.core.ApiType\"\xa1\x01\n\x10\x42videoBAudioItem\x12\x12\n\nquality_id\x18\x01 \x01(\r\x12\x14\n\x0cquality_text\x18\x02 \x01(\t\x12\x12\n\ncodec_text\x18\x03 \x01(\t\x12\x10\n\x08\x62it_rate\x18\x04 \x01(\t\x12\x13\n\x0bstream_size\x18\x05 \x01(\t\x12(\n\x08\x61pi_type\x18\x06 \x01(\x0e\x32\x16.jijidown.core.ApiType\"w\n\x15\x42videoAllQualityReply\x12.\n\x05video\x18\x01 \x03(\x0b\x32\x1f.jijidown.core.BvideoBVideoItem\x12.\n\x05\x61udio\x18\x02 \x03(\x0b\x32\x1f.jijidown.core.BvideoBAudioItem2\x82\x02\n\x06\x42video\x12W\n\x0c\x43heckContent\x12\x1f.jijidown.core.BvideoContentReq\x1a&.jijidown.core.BvideoCheckContentReply\x12G\n\x04Info\x12\x1f.jijidown.core.BvideoContentReq\x1a\x1e.jijidown.core.BvideoInfoReply\x12V\n\nAllQuality\x12\".jijidown.core.BvideoAllQualityReq\x1a$.jijidown.core.BvideoAllQualityReplyBIZ3github.com/JiJiDown/JiJiDownCore-go/common/jijidown\xaa\x02\x11JiJiDown.Core.SDKb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'bvideo_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z3github.com/JiJiDown/JiJiDownCore-go/common/jijidown\252\002\021JiJiDown.Core.SDK'
  _globals['_BVIDEOCONTENTREQ']._serialized_start=89
  _globals['_BVIDEOCONTENTREQ']._serialized_end=124
  _globals['_BVIDEOCHECKCONTENTREPLY']._serialized_start=126
  _globals['_BVIDEOCHECKCONTENTREPLY']._serialized_end=219
  _globals['_BVIDEOINFOREPLY']._serialized_start=222
  _globals['_BVIDEOINFOREPLY']._serialized_end=549
  _globals['_BVIDEOBLOCK']._serialized_start=551
  _globals['_BVIDEOBLOCK']._serialized_end=626
  _globals['_BVIDEOPAGE']._serialized_start=629
  _globals['_BVIDEOPAGE']._serialized_end=772
  _globals['_BVIDEOALLQUALITYREQ']._serialized_start=774
  _globals['_BVIDEOALLQUALITYREQ']._serialized_end=835
  _globals['_BVIDEOBVIDEOITEM']._serialized_start=838
  _globals['_BVIDEOBVIDEOITEM']._serialized_end=1040
  _globals['_BVIDEOBAUDIOITEM']._serialized_start=1043
  _globals['_BVIDEOBAUDIOITEM']._serialized_end=1204
  _globals['_BVIDEOALLQUALITYREPLY']._serialized_start=1206
  _globals['_BVIDEOALLQUALITYREPLY']._serialized_end=1325
  _globals['_BVIDEO']._serialized_start=1328
  _globals['_BVIDEO']._serialized_end=1586
# @@protoc_insertion_point(module_scope)
