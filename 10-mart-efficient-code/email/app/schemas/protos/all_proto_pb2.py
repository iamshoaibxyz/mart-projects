# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: all_proto.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'all_proto.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0f\x61ll_proto.proto\x12\x06models\"\xf4\x01\n\x07\x43ompany\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\r\n\x05\x65mail\x18\x04 \x01(\t\x12\x10\n\x08password\x18\x05 \x01(\t\x12\x13\n\x0bis_verified\x18\x06 \x01(\x08\x12\x13\n\x0bverified_at\x18\x07 \x01(\t\x12\x12\n\ncreated_at\x18\x08 \x01(\t\x12\x12\n\nupdated_at\x18\t \x01(\t\x12$\n\x06tokens\x18\n \x03(\x0b\x32\x14.models.CompanyToken\x12!\n\x08products\x18\x0b \x03(\x0b\x32\x0f.models.Product\"e\n\x0c\x43ompanyToken\x12\n\n\x02id\x18\x01 \x01(\t\x12\x12\n\ncompany_id\x18\x02 \x01(\t\x12\r\n\x05token\x18\x03 \x01(\t\x12\x12\n\ncreated_at\x18\x04 \x01(\t\x12\x12\n\nexpired_at\x18\x05 \x01(\t\"\xae\x02\n\x04User\x12\n\n\x02id\x18\x01 \x01(\t\x12\x12\n\nfirst_name\x18\x02 \x01(\t\x12\x11\n\tlast_name\x18\x03 \x01(\t\x12\x10\n\x08password\x18\x04 \x01(\t\x12\r\n\x05\x65mail\x18\x05 \x01(\t\x12\x13\n\x0bis_verified\x18\x06 \x01(\x08\x12\x13\n\x0bverified_at\x18\x07 \x01(\t\x12\x12\n\ncreated_at\x18\x08 \x01(\t\x12\x12\n\nupdated_at\x18\t \x01(\t\x12!\n\x06tokens\x18\n \x03(\x0b\x32\x11.models.UserToken\x12\x1d\n\x06orders\x18\x0b \x03(\x0b\x32\r.models.Order\x12!\n\x08\x63omments\x18\x0c \x03(\x0b\x32\x0f.models.Comment\x12\x1b\n\x05\x63\x61rts\x18\r \x03(\x0b\x32\x0c.models.Cart\"_\n\tUserToken\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x07user_id\x18\x02 \x01(\t\x12\r\n\x05token\x18\x03 \x01(\t\x12\x12\n\ncreated_at\x18\x04 \x01(\t\x12\x12\n\nexpired_at\x18\x05 \x01(\t\"\x88\x01\n\x07\x43omment\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x07user_id\x18\x02 \x01(\t\x12\x12\n\nproduct_id\x18\x03 \x01(\t\x12\x14\n\x0c\x63omment_text\x18\x04 \x01(\t\x12\x0e\n\x06rating\x18\x05 \x01(\x02\x12\x12\n\ncreated_at\x18\x06 \x01(\t\x12\x12\n\nupdated_at\x18\x07 \x01(\t\"\x86\x01\n\x05\x45mail\x12\n\n\x02id\x18\x01 \x01(\t\x12\x17\n\x0frecipient_email\x18\x02 \x01(\t\x12\x0f\n\x07subject\x18\x03 \x01(\t\x12\x0f\n\x07sent_at\x18\x04 \x01(\t\x12\x0e\n\x06status\x18\x05 \x01(\t\x12&\n\x08\x63ontents\x18\x06 \x03(\x0b\x32\x14.models.EmailContent\"=\n\x0c\x45mailContent\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\t\x12\x10\n\x08\x65mail_id\x18\x03 \x01(\t\"\xc7\x02\n\x07Product\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\r\n\x05price\x18\x04 \x01(\x02\x12\x10\n\x08\x63\x61tegory\x18\x05 \x01(\t\x12\x12\n\ncompany_id\x18\x06 \x01(\t\x12\x17\n\x0fproduct_ranking\x18\x07 \x01(\x02\x12\x12\n\ncreated_at\x18\x08 \x01(\t\x12\x12\n\nupdated_at\x18\t \x01(\t\x12!\n\x08\x63omments\x18\n \x03(\x0b\x32\x0f.models.Comment\x12\x1d\n\x06orders\x18\x0b \x03(\x0b\x32\r.models.Order\x12!\n\x05stock\x18\x0c \x01(\x0b\x32\x12.models.StockLevel\x12\x32\n\x0ctransactions\x18\r \x03(\x0b\x32\x1c.models.InventoryTransaction\"\x8f\x01\n\x04\x43\x61rt\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x07user_id\x18\x02 \x01(\t\x12\x0e\n\x06status\x18\x03 \x01(\t\x12\x12\n\ncreated_at\x18\x04 \x01(\t\x12\x12\n\nupdated_at\x18\x05 \x01(\t\x12\x13\n\x0btotal_price\x18\x06 \x01(\x02\x12\x1d\n\x06orders\x18\x07 \x03(\x0b\x32\r.models.Order\"\xac\x02\n\x05Order\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x07\x63\x61rt_id\x18\x02 \x01(\t\x12\x0f\n\x07user_id\x18\x03 \x01(\t\x12\x12\n\nproduct_id\x18\x04 \x01(\t\x12\x15\n\rproduct_price\x18\x05 \x01(\x02\x12\x10\n\x08quantity\x18\x06 \x01(\x05\x12\x13\n\x0btotal_price\x18\x07 \x01(\x02\x12\x12\n\norder_date\x18\x08 \x01(\t\x12\x15\n\rdelivery_date\x18\t \x01(\t\x12\x11\n\tdelivered\x18\n \x01(\x08\x12\x0e\n\x06status\x18\x0b \x01(\t\x12\x13\n\x0breturn_back\x18\x0c \x01(\t\x12\x18\n\x10\x64\x65livery_address\x18\r \x01(\t\x12\x12\n\ncreated_at\x18\x0e \x01(\t\x12\x12\n\nupdated_at\x18\x0f \x01(\t\"\xc5\x01\n\x14InventoryTransaction\x12\n\n\x02id\x18\x01 \x01(\t\x12\x10\n\x08stock_id\x18\x02 \x01(\t\x12\x12\n\nproduct_id\x18\x03 \x01(\t\x12\x10\n\x08quantity\x18\x04 \x01(\x05\x12\x11\n\ttimestamp\x18\x05 \x01(\t\x12\x11\n\toperation\x18\x06 \x01(\t\x12 \n\x07product\x18\x07 \x01(\x0b\x32\x0f.models.Product\x12!\n\x05stock\x18\x08 \x01(\x0b\x32\x12.models.StockLevel\"\x9a\x01\n\nStockLevel\x12\n\n\x02id\x18\x01 \x01(\t\x12\x12\n\nproduct_id\x18\x02 \x01(\t\x12\x10\n\x08quantity\x18\x03 \x01(\x05\x12\x12\n\nupdated_at\x18\x04 \x01(\t\x12\x12\n\ncreated_at\x18\x05 \x01(\t\x12\x32\n\x0ctransactions\x18\x06 \x03(\x0b\x32\x1c.models.InventoryTransaction\"\xc6\x01\n\x10ProductWithStock\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\r\n\x05price\x18\x04 \x01(\x02\x12\x10\n\x08\x63\x61tegory\x18\x05 \x01(\t\x12\x12\n\ncompany_id\x18\x06 \x01(\t\x12\x17\n\x0fproduct_ranking\x18\x07 \x01(\x02\x12\x12\n\ncreated_at\x18\x08 \x01(\t\x12\x12\n\nupdated_at\x18\t \x01(\t\x12\r\n\x05stock\x18\n \x01(\tb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'all_proto_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_COMPANY']._serialized_start=28
  _globals['_COMPANY']._serialized_end=272
  _globals['_COMPANYTOKEN']._serialized_start=274
  _globals['_COMPANYTOKEN']._serialized_end=375
  _globals['_USER']._serialized_start=378
  _globals['_USER']._serialized_end=680
  _globals['_USERTOKEN']._serialized_start=682
  _globals['_USERTOKEN']._serialized_end=777
  _globals['_COMMENT']._serialized_start=780
  _globals['_COMMENT']._serialized_end=916
  _globals['_EMAIL']._serialized_start=919
  _globals['_EMAIL']._serialized_end=1053
  _globals['_EMAILCONTENT']._serialized_start=1055
  _globals['_EMAILCONTENT']._serialized_end=1116
  _globals['_PRODUCT']._serialized_start=1119
  _globals['_PRODUCT']._serialized_end=1446
  _globals['_CART']._serialized_start=1449
  _globals['_CART']._serialized_end=1592
  _globals['_ORDER']._serialized_start=1595
  _globals['_ORDER']._serialized_end=1895
  _globals['_INVENTORYTRANSACTION']._serialized_start=1898
  _globals['_INVENTORYTRANSACTION']._serialized_end=2095
  _globals['_STOCKLEVEL']._serialized_start=2098
  _globals['_STOCKLEVEL']._serialized_end=2252
  _globals['_PRODUCTWITHSTOCK']._serialized_start=2255
  _globals['_PRODUCTWITHSTOCK']._serialized_end=2453
# @@protoc_insertion_point(module_scope)
