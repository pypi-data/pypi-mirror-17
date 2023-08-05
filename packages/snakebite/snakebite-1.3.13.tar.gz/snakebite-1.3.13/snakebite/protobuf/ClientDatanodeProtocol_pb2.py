# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import service
from google.protobuf import service_reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)


import hdfs_pb2

DESCRIPTOR = descriptor.FileDescriptor(
  name='ClientDatanodeProtocol.proto',
  package='',
  serialized_pb='\n\x1c\x43lientDatanodeProtocol.proto\x1a\nhdfs.proto\"I\n#GetReplicaVisibleLengthRequestProto\x12\"\n\x05\x62lock\x18\x01 \x02(\x0b\x32\x13.ExtendedBlockProto\"6\n$GetReplicaVisibleLengthResponseProto\x12\x0e\n\x06length\x18\x01 \x02(\x04\"\x1e\n\x1cRefreshNamenodesRequestProto\"\x1f\n\x1dRefreshNamenodesResponseProto\"?\n\x1b\x44\x65leteBlockPoolRequestProto\x12\x11\n\tblockPool\x18\x01 \x02(\t\x12\r\n\x05\x66orce\x18\x02 \x02(\x08\"\x1e\n\x1c\x44\x65leteBlockPoolResponseProto\"r\n!GetBlockLocalPathInfoRequestProto\x12\"\n\x05\x62lock\x18\x01 \x02(\x0b\x32\x13.ExtendedBlockProto\x12)\n\x05token\x18\x02 \x02(\x0b\x32\x1a.BlockTokenIdentifierProto\"r\n\"GetBlockLocalPathInfoResponseProto\x12\"\n\x05\x62lock\x18\x01 \x02(\x0b\x32\x13.ExtendedBlockProto\x12\x11\n\tlocalPath\x18\x02 \x02(\t\x12\x15\n\rlocalMetaPath\x18\x03 \x02(\t\"t\n!GetHdfsBlockLocationsRequestProto\x12#\n\x06\x62locks\x18\x01 \x03(\x0b\x32\x13.ExtendedBlockProto\x12*\n\x06tokens\x18\x02 \x03(\x0b\x32\x1a.BlockTokenIdentifierProto\"N\n\"GetHdfsBlockLocationsResponseProto\x12\x11\n\tvolumeIds\x18\x01 \x03(\x0c\x12\x15\n\rvolumeIndexes\x18\x02 \x03(\r2\xee\x03\n\x1d\x43lientDatanodeProtocolService\x12\x66\n\x17getReplicaVisibleLength\x12$.GetReplicaVisibleLengthRequestProto\x1a%.GetReplicaVisibleLengthResponseProto\x12Q\n\x10refreshNamenodes\x12\x1d.RefreshNamenodesRequestProto\x1a\x1e.RefreshNamenodesResponseProto\x12N\n\x0f\x64\x65leteBlockPool\x12\x1c.DeleteBlockPoolRequestProto\x1a\x1d.DeleteBlockPoolResponseProto\x12`\n\x15getBlockLocalPathInfo\x12\".GetBlockLocalPathInfoRequestProto\x1a#.GetBlockLocalPathInfoResponseProto\x12`\n\x15getHdfsBlockLocations\x12\".GetHdfsBlockLocationsRequestProto\x1a#.GetHdfsBlockLocationsResponseProtoBN\n%org.apache.hadoop.hdfs.protocol.protoB\x1c\x43lientDatanodeProtocolProtos\x88\x01\x01\x90\x01\x01\xa0\x01\x01')




_GETREPLICAVISIBLELENGTHREQUESTPROTO = descriptor.Descriptor(
  name='GetReplicaVisibleLengthRequestProto',
  full_name='GetReplicaVisibleLengthRequestProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='block', full_name='GetReplicaVisibleLengthRequestProto.block', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
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
  serialized_start=44,
  serialized_end=117,
)


_GETREPLICAVISIBLELENGTHRESPONSEPROTO = descriptor.Descriptor(
  name='GetReplicaVisibleLengthResponseProto',
  full_name='GetReplicaVisibleLengthResponseProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='length', full_name='GetReplicaVisibleLengthResponseProto.length', index=0,
      number=1, type=4, cpp_type=4, label=2,
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
  serialized_start=119,
  serialized_end=173,
)


_REFRESHNAMENODESREQUESTPROTO = descriptor.Descriptor(
  name='RefreshNamenodesRequestProto',
  full_name='RefreshNamenodesRequestProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=175,
  serialized_end=205,
)


_REFRESHNAMENODESRESPONSEPROTO = descriptor.Descriptor(
  name='RefreshNamenodesResponseProto',
  full_name='RefreshNamenodesResponseProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=207,
  serialized_end=238,
)


_DELETEBLOCKPOOLREQUESTPROTO = descriptor.Descriptor(
  name='DeleteBlockPoolRequestProto',
  full_name='DeleteBlockPoolRequestProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='blockPool', full_name='DeleteBlockPoolRequestProto.blockPool', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='force', full_name='DeleteBlockPoolRequestProto.force', index=1,
      number=2, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
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
  serialized_start=240,
  serialized_end=303,
)


_DELETEBLOCKPOOLRESPONSEPROTO = descriptor.Descriptor(
  name='DeleteBlockPoolResponseProto',
  full_name='DeleteBlockPoolResponseProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=305,
  serialized_end=335,
)


_GETBLOCKLOCALPATHINFOREQUESTPROTO = descriptor.Descriptor(
  name='GetBlockLocalPathInfoRequestProto',
  full_name='GetBlockLocalPathInfoRequestProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='block', full_name='GetBlockLocalPathInfoRequestProto.block', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='token', full_name='GetBlockLocalPathInfoRequestProto.token', index=1,
      number=2, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
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
  serialized_start=337,
  serialized_end=451,
)


_GETBLOCKLOCALPATHINFORESPONSEPROTO = descriptor.Descriptor(
  name='GetBlockLocalPathInfoResponseProto',
  full_name='GetBlockLocalPathInfoResponseProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='block', full_name='GetBlockLocalPathInfoResponseProto.block', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='localPath', full_name='GetBlockLocalPathInfoResponseProto.localPath', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='localMetaPath', full_name='GetBlockLocalPathInfoResponseProto.localMetaPath', index=2,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
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
  serialized_start=453,
  serialized_end=567,
)


_GETHDFSBLOCKLOCATIONSREQUESTPROTO = descriptor.Descriptor(
  name='GetHdfsBlockLocationsRequestProto',
  full_name='GetHdfsBlockLocationsRequestProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='blocks', full_name='GetHdfsBlockLocationsRequestProto.blocks', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='tokens', full_name='GetHdfsBlockLocationsRequestProto.tokens', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=569,
  serialized_end=685,
)


_GETHDFSBLOCKLOCATIONSRESPONSEPROTO = descriptor.Descriptor(
  name='GetHdfsBlockLocationsResponseProto',
  full_name='GetHdfsBlockLocationsResponseProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='volumeIds', full_name='GetHdfsBlockLocationsResponseProto.volumeIds', index=0,
      number=1, type=12, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='volumeIndexes', full_name='GetHdfsBlockLocationsResponseProto.volumeIndexes', index=1,
      number=2, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=687,
  serialized_end=765,
)

_GETREPLICAVISIBLELENGTHREQUESTPROTO.fields_by_name['block'].message_type = hdfs_pb2._EXTENDEDBLOCKPROTO
_GETBLOCKLOCALPATHINFOREQUESTPROTO.fields_by_name['block'].message_type = hdfs_pb2._EXTENDEDBLOCKPROTO
_GETBLOCKLOCALPATHINFOREQUESTPROTO.fields_by_name['token'].message_type = hdfs_pb2._BLOCKTOKENIDENTIFIERPROTO
_GETBLOCKLOCALPATHINFORESPONSEPROTO.fields_by_name['block'].message_type = hdfs_pb2._EXTENDEDBLOCKPROTO
_GETHDFSBLOCKLOCATIONSREQUESTPROTO.fields_by_name['blocks'].message_type = hdfs_pb2._EXTENDEDBLOCKPROTO
_GETHDFSBLOCKLOCATIONSREQUESTPROTO.fields_by_name['tokens'].message_type = hdfs_pb2._BLOCKTOKENIDENTIFIERPROTO
DESCRIPTOR.message_types_by_name['GetReplicaVisibleLengthRequestProto'] = _GETREPLICAVISIBLELENGTHREQUESTPROTO
DESCRIPTOR.message_types_by_name['GetReplicaVisibleLengthResponseProto'] = _GETREPLICAVISIBLELENGTHRESPONSEPROTO
DESCRIPTOR.message_types_by_name['RefreshNamenodesRequestProto'] = _REFRESHNAMENODESREQUESTPROTO
DESCRIPTOR.message_types_by_name['RefreshNamenodesResponseProto'] = _REFRESHNAMENODESRESPONSEPROTO
DESCRIPTOR.message_types_by_name['DeleteBlockPoolRequestProto'] = _DELETEBLOCKPOOLREQUESTPROTO
DESCRIPTOR.message_types_by_name['DeleteBlockPoolResponseProto'] = _DELETEBLOCKPOOLRESPONSEPROTO
DESCRIPTOR.message_types_by_name['GetBlockLocalPathInfoRequestProto'] = _GETBLOCKLOCALPATHINFOREQUESTPROTO
DESCRIPTOR.message_types_by_name['GetBlockLocalPathInfoResponseProto'] = _GETBLOCKLOCALPATHINFORESPONSEPROTO
DESCRIPTOR.message_types_by_name['GetHdfsBlockLocationsRequestProto'] = _GETHDFSBLOCKLOCATIONSREQUESTPROTO
DESCRIPTOR.message_types_by_name['GetHdfsBlockLocationsResponseProto'] = _GETHDFSBLOCKLOCATIONSRESPONSEPROTO

class GetReplicaVisibleLengthRequestProto(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _GETREPLICAVISIBLELENGTHREQUESTPROTO
  
  # @@protoc_insertion_point(class_scope:GetReplicaVisibleLengthRequestProto)

class GetReplicaVisibleLengthResponseProto(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _GETREPLICAVISIBLELENGTHRESPONSEPROTO
  
  # @@protoc_insertion_point(class_scope:GetReplicaVisibleLengthResponseProto)

class RefreshNamenodesRequestProto(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _REFRESHNAMENODESREQUESTPROTO
  
  # @@protoc_insertion_point(class_scope:RefreshNamenodesRequestProto)

class RefreshNamenodesResponseProto(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _REFRESHNAMENODESRESPONSEPROTO
  
  # @@protoc_insertion_point(class_scope:RefreshNamenodesResponseProto)

class DeleteBlockPoolRequestProto(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _DELETEBLOCKPOOLREQUESTPROTO
  
  # @@protoc_insertion_point(class_scope:DeleteBlockPoolRequestProto)

class DeleteBlockPoolResponseProto(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _DELETEBLOCKPOOLRESPONSEPROTO
  
  # @@protoc_insertion_point(class_scope:DeleteBlockPoolResponseProto)

class GetBlockLocalPathInfoRequestProto(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _GETBLOCKLOCALPATHINFOREQUESTPROTO
  
  # @@protoc_insertion_point(class_scope:GetBlockLocalPathInfoRequestProto)

class GetBlockLocalPathInfoResponseProto(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _GETBLOCKLOCALPATHINFORESPONSEPROTO
  
  # @@protoc_insertion_point(class_scope:GetBlockLocalPathInfoResponseProto)

class GetHdfsBlockLocationsRequestProto(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _GETHDFSBLOCKLOCATIONSREQUESTPROTO
  
  # @@protoc_insertion_point(class_scope:GetHdfsBlockLocationsRequestProto)

class GetHdfsBlockLocationsResponseProto(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _GETHDFSBLOCKLOCATIONSRESPONSEPROTO
  
  # @@protoc_insertion_point(class_scope:GetHdfsBlockLocationsResponseProto)


_CLIENTDATANODEPROTOCOLSERVICE = descriptor.ServiceDescriptor(
  name='ClientDatanodeProtocolService',
  full_name='ClientDatanodeProtocolService',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=768,
  serialized_end=1262,
  methods=[
  descriptor.MethodDescriptor(
    name='getReplicaVisibleLength',
    full_name='ClientDatanodeProtocolService.getReplicaVisibleLength',
    index=0,
    containing_service=None,
    input_type=_GETREPLICAVISIBLELENGTHREQUESTPROTO,
    output_type=_GETREPLICAVISIBLELENGTHRESPONSEPROTO,
    options=None,
  ),
  descriptor.MethodDescriptor(
    name='refreshNamenodes',
    full_name='ClientDatanodeProtocolService.refreshNamenodes',
    index=1,
    containing_service=None,
    input_type=_REFRESHNAMENODESREQUESTPROTO,
    output_type=_REFRESHNAMENODESRESPONSEPROTO,
    options=None,
  ),
  descriptor.MethodDescriptor(
    name='deleteBlockPool',
    full_name='ClientDatanodeProtocolService.deleteBlockPool',
    index=2,
    containing_service=None,
    input_type=_DELETEBLOCKPOOLREQUESTPROTO,
    output_type=_DELETEBLOCKPOOLRESPONSEPROTO,
    options=None,
  ),
  descriptor.MethodDescriptor(
    name='getBlockLocalPathInfo',
    full_name='ClientDatanodeProtocolService.getBlockLocalPathInfo',
    index=3,
    containing_service=None,
    input_type=_GETBLOCKLOCALPATHINFOREQUESTPROTO,
    output_type=_GETBLOCKLOCALPATHINFORESPONSEPROTO,
    options=None,
  ),
  descriptor.MethodDescriptor(
    name='getHdfsBlockLocations',
    full_name='ClientDatanodeProtocolService.getHdfsBlockLocations',
    index=4,
    containing_service=None,
    input_type=_GETHDFSBLOCKLOCATIONSREQUESTPROTO,
    output_type=_GETHDFSBLOCKLOCATIONSRESPONSEPROTO,
    options=None,
  ),
])

class ClientDatanodeProtocolService(service.Service):
  __metaclass__ = service_reflection.GeneratedServiceType
  DESCRIPTOR = _CLIENTDATANODEPROTOCOLSERVICE
class ClientDatanodeProtocolService_Stub(ClientDatanodeProtocolService):
  __metaclass__ = service_reflection.GeneratedServiceStubType
  DESCRIPTOR = _CLIENTDATANODEPROTOCOLSERVICE

# @@protoc_insertion_point(module_scope)
