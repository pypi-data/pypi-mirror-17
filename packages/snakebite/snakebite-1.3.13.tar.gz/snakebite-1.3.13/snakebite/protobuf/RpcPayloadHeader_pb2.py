# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)



DESCRIPTOR = descriptor.FileDescriptor(
  name='RpcPayloadHeader.proto',
  package='',
  serialized_pb='\n\x16RpcPayloadHeader.proto\"q\n\x15RpcPayloadHeaderProto\x12\x1e\n\x07rpcKind\x18\x01 \x01(\x0e\x32\r.RpcKindProto\x12(\n\x05rpcOp\x18\x02 \x01(\x0e\x32\x19.RpcPayloadOperationProto\x12\x0e\n\x06\x63\x61llId\x18\x03 \x02(\r\"f\n\x16RpcResponseHeaderProto\x12\x0e\n\x06\x63\x61llId\x18\x01 \x02(\r\x12\x1f\n\x06status\x18\x02 \x02(\x0e\x32\x0f.RpcStatusProto\x12\x1b\n\x13serverIpcVersionNum\x18\x03 \x01(\r*J\n\x0cRpcKindProto\x12\x0f\n\x0bRPC_BUILTIN\x10\x00\x12\x10\n\x0cRPC_WRITABLE\x10\x01\x12\x17\n\x13RPC_PROTOCOL_BUFFER\x10\x02*i\n\x18RpcPayloadOperationProto\x12\x15\n\x11RPC_FINAL_PAYLOAD\x10\x00\x12\x1c\n\x18RPC_CONTINUATION_PAYLOAD\x10\x01\x12\x18\n\x14RPC_CLOSE_CONNECTION\x10\x02*3\n\x0eRpcStatusProto\x12\x0b\n\x07SUCCESS\x10\x00\x12\t\n\x05\x45RROR\x10\x01\x12\t\n\x05\x46\x41TAL\x10\x02\x42;\n\x1eorg.apache.hadoop.ipc.protobufB\x16RpcPayloadHeaderProtos\xa0\x01\x01')

_RPCKINDPROTO = descriptor.EnumDescriptor(
  name='RpcKindProto',
  full_name='RpcKindProto',
  filename=None,
  file=DESCRIPTOR,
  values=[
    descriptor.EnumValueDescriptor(
      name='RPC_BUILTIN', index=0, number=0,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='RPC_WRITABLE', index=1, number=1,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='RPC_PROTOCOL_BUFFER', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=245,
  serialized_end=319,
)


_RPCPAYLOADOPERATIONPROTO = descriptor.EnumDescriptor(
  name='RpcPayloadOperationProto',
  full_name='RpcPayloadOperationProto',
  filename=None,
  file=DESCRIPTOR,
  values=[
    descriptor.EnumValueDescriptor(
      name='RPC_FINAL_PAYLOAD', index=0, number=0,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='RPC_CONTINUATION_PAYLOAD', index=1, number=1,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='RPC_CLOSE_CONNECTION', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=321,
  serialized_end=426,
)


_RPCSTATUSPROTO = descriptor.EnumDescriptor(
  name='RpcStatusProto',
  full_name='RpcStatusProto',
  filename=None,
  file=DESCRIPTOR,
  values=[
    descriptor.EnumValueDescriptor(
      name='SUCCESS', index=0, number=0,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='ERROR', index=1, number=1,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='FATAL', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=428,
  serialized_end=479,
)


RPC_BUILTIN = 0
RPC_WRITABLE = 1
RPC_PROTOCOL_BUFFER = 2
RPC_FINAL_PAYLOAD = 0
RPC_CONTINUATION_PAYLOAD = 1
RPC_CLOSE_CONNECTION = 2
SUCCESS = 0
ERROR = 1
FATAL = 2



_RPCPAYLOADHEADERPROTO = descriptor.Descriptor(
  name='RpcPayloadHeaderProto',
  full_name='RpcPayloadHeaderProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='rpcKind', full_name='RpcPayloadHeaderProto.rpcKind', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='rpcOp', full_name='RpcPayloadHeaderProto.rpcOp', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='callId', full_name='RpcPayloadHeaderProto.callId', index=2,
      number=3, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=26,
  serialized_end=139,
)


_RPCRESPONSEHEADERPROTO = descriptor.Descriptor(
  name='RpcResponseHeaderProto',
  full_name='RpcResponseHeaderProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='callId', full_name='RpcResponseHeaderProto.callId', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='status', full_name='RpcResponseHeaderProto.status', index=1,
      number=2, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='serverIpcVersionNum', full_name='RpcResponseHeaderProto.serverIpcVersionNum', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=141,
  serialized_end=243,
)

_RPCPAYLOADHEADERPROTO.fields_by_name['rpcKind'].enum_type = _RPCKINDPROTO
_RPCPAYLOADHEADERPROTO.fields_by_name['rpcOp'].enum_type = _RPCPAYLOADOPERATIONPROTO
_RPCRESPONSEHEADERPROTO.fields_by_name['status'].enum_type = _RPCSTATUSPROTO
DESCRIPTOR.message_types_by_name['RpcPayloadHeaderProto'] = _RPCPAYLOADHEADERPROTO
DESCRIPTOR.message_types_by_name['RpcResponseHeaderProto'] = _RPCRESPONSEHEADERPROTO

class RpcPayloadHeaderProto(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RPCPAYLOADHEADERPROTO
  
  # @@protoc_insertion_point(class_scope:RpcPayloadHeaderProto)

class RpcResponseHeaderProto(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RPCRESPONSEHEADERPROTO
  
  # @@protoc_insertion_point(class_scope:RpcResponseHeaderProto)

# @@protoc_insertion_point(module_scope)
