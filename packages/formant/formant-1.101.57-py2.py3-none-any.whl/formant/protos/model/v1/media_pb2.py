# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protos/model/v1/media.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from formant.protos.model.v1 import math_pb2 as protos_dot_model_dot_v1_dot_math__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='protos/model/v1/media.proto',
  package='v1.model',
  syntax='proto3',
  serialized_options=b'Z)github.com/FormantIO/genproto/go/v1/model',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1bprotos/model/v1/media.proto\x12\x08v1.model\x1a\x1aprotos/model/v1/math.proto\"Z\n\x05Image\x12!\n\x0c\x63ontent_type\x18\x01 \x01(\tR\x0b\x63ontentType\x12\x12\n\x03url\x18\x02 \x01(\tH\x00R\x03url\x12\x12\n\x03raw\x18\x03 \x01(\x0cH\x00R\x03rawB\x06\n\x04\x64\x61ta\"\x8b\x01\n\nPointCloud\x12\x12\n\x04uuid\x18\x04 \x01(\tR\x04uuid\x12\x12\n\x03url\x18\x01 \x01(\tH\x00R\x03url\x12\x12\n\x03raw\x18\x02 \x01(\x0cH\x00R\x03raw\x12\x39\n\x0eworld_to_local\x18\x03 \x01(\x0b\x32\x13.v1.model.TransformR\x0cworldToLocalB\x06\n\x04\x64\x61ta\"^\n\rRtcPointCloud\x12\x12\n\x04\x64\x61ta\x18\x01 \x01(\x0cR\x04\x64\x61ta\x12\x39\n\x0eworld_to_local\x18\x02 \x01(\x0b\x32\x13.v1.model.TransformR\x0cworldToLocal\"[\n\x0eH264VideoFrame\x12\x14\n\x05index\x18\x01 \x01(\x05R\x05index\x12\x14\n\x05\x66lags\x18\x02 \x01(\x05R\x05\x66lags\x12\x1d\n\nframe_data\x18\x03 \x01(\x0cR\tframeData\"Y\n\nAudioChunk\x12\x14\n\x05index\x18\x01 \x01(\x05R\x05index\x12\x16\n\x06\x66ormat\x18\x02 \x01(\tR\x06\x66ormat\x12\x1d\n\nchunk_data\x18\x03 \x01(\x0cR\tchunkData\"p\n\x05Video\x12\x1b\n\tmime_type\x18\x01 \x01(\tR\x08mimeType\x12\x1a\n\x08\x64uration\x18\x02 \x01(\x03R\x08\x64uration\x12\x12\n\x03url\x18\x03 \x01(\tH\x00R\x03url\x12\x12\n\x03raw\x18\x04 \x01(\x0cH\x00R\x03rawB\x06\n\x04\x64\x61ta\"?\n\rTransformTree\x12\x12\n\x03url\x18\x01 \x01(\tH\x00R\x03url\x12\x12\n\x03raw\x18\x02 \x01(\x0cH\x00R\x03rawB\x06\n\x04\x64\x61taB+Z)github.com/FormantIO/genproto/go/v1/modelb\x06proto3'
  ,
  dependencies=[protos_dot_model_dot_v1_dot_math__pb2.DESCRIPTOR,])




_IMAGE = _descriptor.Descriptor(
  name='Image',
  full_name='v1.model.Image',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='content_type', full_name='v1.model.Image.content_type', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='contentType', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='url', full_name='v1.model.Image.url', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='url', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='raw', full_name='v1.model.Image.raw', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='raw', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='data', full_name='v1.model.Image.data',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=69,
  serialized_end=159,
)


_POINTCLOUD = _descriptor.Descriptor(
  name='PointCloud',
  full_name='v1.model.PointCloud',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='uuid', full_name='v1.model.PointCloud.uuid', index=0,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='uuid', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='url', full_name='v1.model.PointCloud.url', index=1,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='url', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='raw', full_name='v1.model.PointCloud.raw', index=2,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='raw', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='world_to_local', full_name='v1.model.PointCloud.world_to_local', index=3,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='worldToLocal', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='data', full_name='v1.model.PointCloud.data',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=162,
  serialized_end=301,
)


_RTCPOINTCLOUD = _descriptor.Descriptor(
  name='RtcPointCloud',
  full_name='v1.model.RtcPointCloud',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='v1.model.RtcPointCloud.data', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='data', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='world_to_local', full_name='v1.model.RtcPointCloud.world_to_local', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='worldToLocal', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=303,
  serialized_end=397,
)


_H264VIDEOFRAME = _descriptor.Descriptor(
  name='H264VideoFrame',
  full_name='v1.model.H264VideoFrame',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='index', full_name='v1.model.H264VideoFrame.index', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='index', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='flags', full_name='v1.model.H264VideoFrame.flags', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='flags', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='frame_data', full_name='v1.model.H264VideoFrame.frame_data', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='frameData', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=399,
  serialized_end=490,
)


_AUDIOCHUNK = _descriptor.Descriptor(
  name='AudioChunk',
  full_name='v1.model.AudioChunk',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='index', full_name='v1.model.AudioChunk.index', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='index', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='format', full_name='v1.model.AudioChunk.format', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='format', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='chunk_data', full_name='v1.model.AudioChunk.chunk_data', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='chunkData', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=492,
  serialized_end=581,
)


_VIDEO = _descriptor.Descriptor(
  name='Video',
  full_name='v1.model.Video',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='mime_type', full_name='v1.model.Video.mime_type', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='mimeType', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='duration', full_name='v1.model.Video.duration', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='duration', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='url', full_name='v1.model.Video.url', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='url', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='raw', full_name='v1.model.Video.raw', index=3,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='raw', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='data', full_name='v1.model.Video.data',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=583,
  serialized_end=695,
)


_TRANSFORMTREE = _descriptor.Descriptor(
  name='TransformTree',
  full_name='v1.model.TransformTree',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='url', full_name='v1.model.TransformTree.url', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='url', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='raw', full_name='v1.model.TransformTree.raw', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='raw', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='data', full_name='v1.model.TransformTree.data',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=697,
  serialized_end=760,
)

_IMAGE.oneofs_by_name['data'].fields.append(
  _IMAGE.fields_by_name['url'])
_IMAGE.fields_by_name['url'].containing_oneof = _IMAGE.oneofs_by_name['data']
_IMAGE.oneofs_by_name['data'].fields.append(
  _IMAGE.fields_by_name['raw'])
_IMAGE.fields_by_name['raw'].containing_oneof = _IMAGE.oneofs_by_name['data']
_POINTCLOUD.fields_by_name['world_to_local'].message_type = protos_dot_model_dot_v1_dot_math__pb2._TRANSFORM
_POINTCLOUD.oneofs_by_name['data'].fields.append(
  _POINTCLOUD.fields_by_name['url'])
_POINTCLOUD.fields_by_name['url'].containing_oneof = _POINTCLOUD.oneofs_by_name['data']
_POINTCLOUD.oneofs_by_name['data'].fields.append(
  _POINTCLOUD.fields_by_name['raw'])
_POINTCLOUD.fields_by_name['raw'].containing_oneof = _POINTCLOUD.oneofs_by_name['data']
_RTCPOINTCLOUD.fields_by_name['world_to_local'].message_type = protos_dot_model_dot_v1_dot_math__pb2._TRANSFORM
_VIDEO.oneofs_by_name['data'].fields.append(
  _VIDEO.fields_by_name['url'])
_VIDEO.fields_by_name['url'].containing_oneof = _VIDEO.oneofs_by_name['data']
_VIDEO.oneofs_by_name['data'].fields.append(
  _VIDEO.fields_by_name['raw'])
_VIDEO.fields_by_name['raw'].containing_oneof = _VIDEO.oneofs_by_name['data']
_TRANSFORMTREE.oneofs_by_name['data'].fields.append(
  _TRANSFORMTREE.fields_by_name['url'])
_TRANSFORMTREE.fields_by_name['url'].containing_oneof = _TRANSFORMTREE.oneofs_by_name['data']
_TRANSFORMTREE.oneofs_by_name['data'].fields.append(
  _TRANSFORMTREE.fields_by_name['raw'])
_TRANSFORMTREE.fields_by_name['raw'].containing_oneof = _TRANSFORMTREE.oneofs_by_name['data']
DESCRIPTOR.message_types_by_name['Image'] = _IMAGE
DESCRIPTOR.message_types_by_name['PointCloud'] = _POINTCLOUD
DESCRIPTOR.message_types_by_name['RtcPointCloud'] = _RTCPOINTCLOUD
DESCRIPTOR.message_types_by_name['H264VideoFrame'] = _H264VIDEOFRAME
DESCRIPTOR.message_types_by_name['AudioChunk'] = _AUDIOCHUNK
DESCRIPTOR.message_types_by_name['Video'] = _VIDEO
DESCRIPTOR.message_types_by_name['TransformTree'] = _TRANSFORMTREE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Image = _reflection.GeneratedProtocolMessageType('Image', (_message.Message,), {
  'DESCRIPTOR' : _IMAGE,
  '__module__' : 'protos.model.v1.media_pb2'
  # @@protoc_insertion_point(class_scope:v1.model.Image)
  })
_sym_db.RegisterMessage(Image)

PointCloud = _reflection.GeneratedProtocolMessageType('PointCloud', (_message.Message,), {
  'DESCRIPTOR' : _POINTCLOUD,
  '__module__' : 'protos.model.v1.media_pb2'
  # @@protoc_insertion_point(class_scope:v1.model.PointCloud)
  })
_sym_db.RegisterMessage(PointCloud)

RtcPointCloud = _reflection.GeneratedProtocolMessageType('RtcPointCloud', (_message.Message,), {
  'DESCRIPTOR' : _RTCPOINTCLOUD,
  '__module__' : 'protos.model.v1.media_pb2'
  # @@protoc_insertion_point(class_scope:v1.model.RtcPointCloud)
  })
_sym_db.RegisterMessage(RtcPointCloud)

H264VideoFrame = _reflection.GeneratedProtocolMessageType('H264VideoFrame', (_message.Message,), {
  'DESCRIPTOR' : _H264VIDEOFRAME,
  '__module__' : 'protos.model.v1.media_pb2'
  # @@protoc_insertion_point(class_scope:v1.model.H264VideoFrame)
  })
_sym_db.RegisterMessage(H264VideoFrame)

AudioChunk = _reflection.GeneratedProtocolMessageType('AudioChunk', (_message.Message,), {
  'DESCRIPTOR' : _AUDIOCHUNK,
  '__module__' : 'protos.model.v1.media_pb2'
  # @@protoc_insertion_point(class_scope:v1.model.AudioChunk)
  })
_sym_db.RegisterMessage(AudioChunk)

Video = _reflection.GeneratedProtocolMessageType('Video', (_message.Message,), {
  'DESCRIPTOR' : _VIDEO,
  '__module__' : 'protos.model.v1.media_pb2'
  # @@protoc_insertion_point(class_scope:v1.model.Video)
  })
_sym_db.RegisterMessage(Video)

TransformTree = _reflection.GeneratedProtocolMessageType('TransformTree', (_message.Message,), {
  'DESCRIPTOR' : _TRANSFORMTREE,
  '__module__' : 'protos.model.v1.media_pb2'
  # @@protoc_insertion_point(class_scope:v1.model.TransformTree)
  })
_sym_db.RegisterMessage(TransformTree)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
