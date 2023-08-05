# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ga4gh/reads.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from ga4gh import common_pb2 as ga4gh_dot_common__pb2
from ga4gh import assay_metadata_pb2 as ga4gh_dot_assay__metadata__pb2
from ga4gh import metadata_pb2 as ga4gh_dot_metadata__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='ga4gh/reads.proto',
  package='ga4gh',
  syntax='proto3',
  serialized_pb=_b('\n\x11ga4gh/reads.proto\x12\x05ga4gh\x1a\x12ga4gh/common.proto\x1a\x1aga4gh/assay_metadata.proto\x1a\x14ga4gh/metadata.proto\x1a\x1cgoogle/protobuf/struct.proto\"Y\n\tReadStats\x12\x1a\n\x12\x61ligned_read_count\x18\x01 \x01(\x03\x12\x1c\n\x14unaligned_read_count\x18\x02 \x01(\x03\x12\x12\n\nbase_count\x18\x03 \x01(\x03\"\xb2\x03\n\tReadGroup\x12\n\n\x02id\x18\x01 \x01(\t\x12\x12\n\ndataset_id\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x04 \x01(\t\x12\x13\n\x0bsample_name\x18\x05 \x01(\t\x12\x15\n\rbio_sample_id\x18\x06 \x01(\t\x12%\n\nexperiment\x18\x07 \x01(\x0b\x32\x11.ga4gh.Experiment\x12\x1d\n\x15predicted_insert_size\x18\x08 \x01(\x05\x12\x0f\n\x07\x63reated\x18\t \x01(\x03\x12\x0f\n\x07updated\x18\n \x01(\x03\x12\x1f\n\x05stats\x18\x0b \x01(\x0b\x32\x10.ga4gh.ReadStats\x12 \n\x08programs\x18\x0c \x03(\x0b\x32\x0e.ga4gh.Program\x12\x18\n\x10reference_set_id\x18\r \x01(\t\x12(\n\x04info\x18\x0e \x03(\x0b\x32\x1a.ga4gh.ReadGroup.InfoEntry\x1aG\n\tInfoEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12)\n\x05value\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.ListValue:\x02\x38\x01\"\x84\x01\n\x0cReadGroupSet\x12\n\n\x02id\x18\x01 \x01(\t\x12\x12\n\ndataset_id\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x1f\n\x05stats\x18\x04 \x01(\x0b\x32\x10.ga4gh.ReadStats\x12%\n\x0bread_groups\x18\x05 \x03(\x0b\x32\x10.ga4gh.ReadGroup\"n\n\x0fLinearAlignment\x12!\n\x08position\x18\x01 \x01(\x0b\x32\x0f.ga4gh.Position\x12\x17\n\x0fmapping_quality\x18\x02 \x01(\x05\x12\x1f\n\x05\x63igar\x18\x03 \x03(\x0b\x32\x10.ga4gh.CigarUnit\"\xab\x04\n\rReadAlignment\x12\n\n\x02id\x18\x01 \x01(\t\x12\x15\n\rread_group_id\x18\x02 \x01(\t\x12\x15\n\rfragment_name\x18\x03 \x01(\t\x12\x1a\n\x12improper_placement\x18\x04 \x01(\x08\x12\x1a\n\x12\x64uplicate_fragment\x18\x05 \x01(\x08\x12\x14\n\x0cnumber_reads\x18\x06 \x01(\x05\x12\x17\n\x0f\x66ragment_length\x18\x07 \x01(\x05\x12\x13\n\x0bread_number\x18\x08 \x01(\x05\x12$\n\x1c\x66\x61iled_vendor_quality_checks\x18\t \x01(\x08\x12)\n\talignment\x18\n \x01(\x0b\x32\x16.ga4gh.LinearAlignment\x12\x1b\n\x13secondary_alignment\x18\x0b \x01(\x08\x12\x1f\n\x17supplementary_alignment\x18\x0c \x01(\x08\x12\x18\n\x10\x61ligned_sequence\x18\r \x01(\t\x12\x17\n\x0f\x61ligned_quality\x18\x0e \x03(\x05\x12+\n\x12next_mate_position\x18\x0f \x01(\x0b\x32\x0f.ga4gh.Position\x12,\n\x04info\x18\x10 \x03(\x0b\x32\x1e.ga4gh.ReadAlignment.InfoEntry\x1aG\n\tInfoEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12)\n\x05value\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.ListValue:\x02\x38\x01\x62\x06proto3')
  ,
  dependencies=[ga4gh_dot_common__pb2.DESCRIPTOR,ga4gh_dot_assay__metadata__pb2.DESCRIPTOR,ga4gh_dot_metadata__pb2.DESCRIPTOR,google_dot_protobuf_dot_struct__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_READSTATS = _descriptor.Descriptor(
  name='ReadStats',
  full_name='ga4gh.ReadStats',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='aligned_read_count', full_name='ga4gh.ReadStats.aligned_read_count', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='unaligned_read_count', full_name='ga4gh.ReadStats.unaligned_read_count', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='base_count', full_name='ga4gh.ReadStats.base_count', index=2,
      number=3, type=3, cpp_type=2, label=1,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=128,
  serialized_end=217,
)


_READGROUP_INFOENTRY = _descriptor.Descriptor(
  name='InfoEntry',
  full_name='ga4gh.ReadGroup.InfoEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='ga4gh.ReadGroup.InfoEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='value', full_name='ga4gh.ReadGroup.InfoEntry.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
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
  options=_descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\001')),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=583,
  serialized_end=654,
)

_READGROUP = _descriptor.Descriptor(
  name='ReadGroup',
  full_name='ga4gh.ReadGroup',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='ga4gh.ReadGroup.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dataset_id', full_name='ga4gh.ReadGroup.dataset_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='name', full_name='ga4gh.ReadGroup.name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='description', full_name='ga4gh.ReadGroup.description', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sample_name', full_name='ga4gh.ReadGroup.sample_name', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bio_sample_id', full_name='ga4gh.ReadGroup.bio_sample_id', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='experiment', full_name='ga4gh.ReadGroup.experiment', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='predicted_insert_size', full_name='ga4gh.ReadGroup.predicted_insert_size', index=7,
      number=8, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='created', full_name='ga4gh.ReadGroup.created', index=8,
      number=9, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='updated', full_name='ga4gh.ReadGroup.updated', index=9,
      number=10, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='stats', full_name='ga4gh.ReadGroup.stats', index=10,
      number=11, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='programs', full_name='ga4gh.ReadGroup.programs', index=11,
      number=12, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='reference_set_id', full_name='ga4gh.ReadGroup.reference_set_id', index=12,
      number=13, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='info', full_name='ga4gh.ReadGroup.info', index=13,
      number=14, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_READGROUP_INFOENTRY, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=220,
  serialized_end=654,
)


_READGROUPSET = _descriptor.Descriptor(
  name='ReadGroupSet',
  full_name='ga4gh.ReadGroupSet',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='ga4gh.ReadGroupSet.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dataset_id', full_name='ga4gh.ReadGroupSet.dataset_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='name', full_name='ga4gh.ReadGroupSet.name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='stats', full_name='ga4gh.ReadGroupSet.stats', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='read_groups', full_name='ga4gh.ReadGroupSet.read_groups', index=4,
      number=5, type=11, cpp_type=10, label=3,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=657,
  serialized_end=789,
)


_LINEARALIGNMENT = _descriptor.Descriptor(
  name='LinearAlignment',
  full_name='ga4gh.LinearAlignment',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='position', full_name='ga4gh.LinearAlignment.position', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='mapping_quality', full_name='ga4gh.LinearAlignment.mapping_quality', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cigar', full_name='ga4gh.LinearAlignment.cigar', index=2,
      number=3, type=11, cpp_type=10, label=3,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=791,
  serialized_end=901,
)


_READALIGNMENT_INFOENTRY = _descriptor.Descriptor(
  name='InfoEntry',
  full_name='ga4gh.ReadAlignment.InfoEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='ga4gh.ReadAlignment.InfoEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='value', full_name='ga4gh.ReadAlignment.InfoEntry.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
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
  options=_descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\001')),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=583,
  serialized_end=654,
)

_READALIGNMENT = _descriptor.Descriptor(
  name='ReadAlignment',
  full_name='ga4gh.ReadAlignment',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='ga4gh.ReadAlignment.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='read_group_id', full_name='ga4gh.ReadAlignment.read_group_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='fragment_name', full_name='ga4gh.ReadAlignment.fragment_name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='improper_placement', full_name='ga4gh.ReadAlignment.improper_placement', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='duplicate_fragment', full_name='ga4gh.ReadAlignment.duplicate_fragment', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='number_reads', full_name='ga4gh.ReadAlignment.number_reads', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='fragment_length', full_name='ga4gh.ReadAlignment.fragment_length', index=6,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='read_number', full_name='ga4gh.ReadAlignment.read_number', index=7,
      number=8, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='failed_vendor_quality_checks', full_name='ga4gh.ReadAlignment.failed_vendor_quality_checks', index=8,
      number=9, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='alignment', full_name='ga4gh.ReadAlignment.alignment', index=9,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='secondary_alignment', full_name='ga4gh.ReadAlignment.secondary_alignment', index=10,
      number=11, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='supplementary_alignment', full_name='ga4gh.ReadAlignment.supplementary_alignment', index=11,
      number=12, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='aligned_sequence', full_name='ga4gh.ReadAlignment.aligned_sequence', index=12,
      number=13, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='aligned_quality', full_name='ga4gh.ReadAlignment.aligned_quality', index=13,
      number=14, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='next_mate_position', full_name='ga4gh.ReadAlignment.next_mate_position', index=14,
      number=15, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='info', full_name='ga4gh.ReadAlignment.info', index=15,
      number=16, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_READALIGNMENT_INFOENTRY, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=904,
  serialized_end=1459,
)

_READGROUP_INFOENTRY.fields_by_name['value'].message_type = google_dot_protobuf_dot_struct__pb2._LISTVALUE
_READGROUP_INFOENTRY.containing_type = _READGROUP
_READGROUP.fields_by_name['experiment'].message_type = ga4gh_dot_assay__metadata__pb2._EXPERIMENT
_READGROUP.fields_by_name['stats'].message_type = _READSTATS
_READGROUP.fields_by_name['programs'].message_type = ga4gh_dot_metadata__pb2._PROGRAM
_READGROUP.fields_by_name['info'].message_type = _READGROUP_INFOENTRY
_READGROUPSET.fields_by_name['stats'].message_type = _READSTATS
_READGROUPSET.fields_by_name['read_groups'].message_type = _READGROUP
_LINEARALIGNMENT.fields_by_name['position'].message_type = ga4gh_dot_common__pb2._POSITION
_LINEARALIGNMENT.fields_by_name['cigar'].message_type = ga4gh_dot_common__pb2._CIGARUNIT
_READALIGNMENT_INFOENTRY.fields_by_name['value'].message_type = google_dot_protobuf_dot_struct__pb2._LISTVALUE
_READALIGNMENT_INFOENTRY.containing_type = _READALIGNMENT
_READALIGNMENT.fields_by_name['alignment'].message_type = _LINEARALIGNMENT
_READALIGNMENT.fields_by_name['next_mate_position'].message_type = ga4gh_dot_common__pb2._POSITION
_READALIGNMENT.fields_by_name['info'].message_type = _READALIGNMENT_INFOENTRY
DESCRIPTOR.message_types_by_name['ReadStats'] = _READSTATS
DESCRIPTOR.message_types_by_name['ReadGroup'] = _READGROUP
DESCRIPTOR.message_types_by_name['ReadGroupSet'] = _READGROUPSET
DESCRIPTOR.message_types_by_name['LinearAlignment'] = _LINEARALIGNMENT
DESCRIPTOR.message_types_by_name['ReadAlignment'] = _READALIGNMENT

ReadStats = _reflection.GeneratedProtocolMessageType('ReadStats', (_message.Message,), dict(
  DESCRIPTOR = _READSTATS,
  __module__ = 'ga4gh.reads_pb2'
  # @@protoc_insertion_point(class_scope:ga4gh.ReadStats)
  ))
_sym_db.RegisterMessage(ReadStats)

ReadGroup = _reflection.GeneratedProtocolMessageType('ReadGroup', (_message.Message,), dict(

  InfoEntry = _reflection.GeneratedProtocolMessageType('InfoEntry', (_message.Message,), dict(
    DESCRIPTOR = _READGROUP_INFOENTRY,
    __module__ = 'ga4gh.reads_pb2'
    # @@protoc_insertion_point(class_scope:ga4gh.ReadGroup.InfoEntry)
    ))
  ,
  DESCRIPTOR = _READGROUP,
  __module__ = 'ga4gh.reads_pb2'
  # @@protoc_insertion_point(class_scope:ga4gh.ReadGroup)
  ))
_sym_db.RegisterMessage(ReadGroup)
_sym_db.RegisterMessage(ReadGroup.InfoEntry)

ReadGroupSet = _reflection.GeneratedProtocolMessageType('ReadGroupSet', (_message.Message,), dict(
  DESCRIPTOR = _READGROUPSET,
  __module__ = 'ga4gh.reads_pb2'
  # @@protoc_insertion_point(class_scope:ga4gh.ReadGroupSet)
  ))
_sym_db.RegisterMessage(ReadGroupSet)

LinearAlignment = _reflection.GeneratedProtocolMessageType('LinearAlignment', (_message.Message,), dict(
  DESCRIPTOR = _LINEARALIGNMENT,
  __module__ = 'ga4gh.reads_pb2'
  # @@protoc_insertion_point(class_scope:ga4gh.LinearAlignment)
  ))
_sym_db.RegisterMessage(LinearAlignment)

ReadAlignment = _reflection.GeneratedProtocolMessageType('ReadAlignment', (_message.Message,), dict(

  InfoEntry = _reflection.GeneratedProtocolMessageType('InfoEntry', (_message.Message,), dict(
    DESCRIPTOR = _READALIGNMENT_INFOENTRY,
    __module__ = 'ga4gh.reads_pb2'
    # @@protoc_insertion_point(class_scope:ga4gh.ReadAlignment.InfoEntry)
    ))
  ,
  DESCRIPTOR = _READALIGNMENT,
  __module__ = 'ga4gh.reads_pb2'
  # @@protoc_insertion_point(class_scope:ga4gh.ReadAlignment)
  ))
_sym_db.RegisterMessage(ReadAlignment)
_sym_db.RegisterMessage(ReadAlignment.InfoEntry)


_READGROUP_INFOENTRY.has_options = True
_READGROUP_INFOENTRY._options = _descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\001'))
_READALIGNMENT_INFOENTRY.has_options = True
_READALIGNMENT_INFOENTRY._options = _descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\001'))
# @@protoc_insertion_point(module_scope)
