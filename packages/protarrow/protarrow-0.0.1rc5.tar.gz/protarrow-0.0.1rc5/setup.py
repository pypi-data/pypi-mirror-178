# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['protarrow']

package_data = \
{'': ['*']}

install_requires = \
['googleapis-common-protos>=1.53.0,<2.0.0',
 'protobuf>=3.20.1,<4.0.0',
 'pyarrow>=8.0.0,<9.0.0']

setup_kwargs = {
    'name': 'protarrow',
    'version': '0.0.1rc5',
    'description': 'Convert from protobuf to arrow and back',
    'long_description': '\n[![codecov](https://codecov.io/gh/0x26res/protarrow/branch/master/graph/badge.svg?token=XMFH27IL70)](https://codecov.io/gh/0x26res/protarrow)\n\n# Protarrow\n\nA library for converting from protobuf to arrow and back \n\n# Installation\n\n```shell\npip install protarrow\n```\n\n# Usage\n\n## Convert from proto to arrow\n\n```protobuf\nmessage MyProto {\n  string name = 1;\n  repeated int32 values = 2;\n}\n```\n\n```python\nimport protarrow\n\nmy_protos = [\n    MyProto(name="foo", values=[1, 2, 4]),\n    MyProto(name="bar", values=[1, 2, 4]),\n]\n\nschema = protarrow.message_type_to_schema(MyProto)\nrecord_batch = protarrow.messages_to_record_batch(my_protos, MyProto)\ntable = protarrow.messages_to_table(my_protos, MyProto)\n```\n\n| name   | values   |\n|:-------|:---------|\n| foo    | [1 2 4]  |\n| bar    | [3 4 5]  |\n\n\n## Convert from arrow to proto\n\n```python\nprotos_from_record_batch = protarrow.table_to_messages(record_batch, MyProto)\nprotos_from_table = protarrow.table_to_messages(table, MyProto)\n```\n\n## Customize arrow type\n\nThe arrow type for `Enum`, `Timestamp` and `TimeOfDay` can be configured:\n\n```python\nconfig = protarrow.ProtarrowConfig(\n    enum_type=pa.int32(),\n    timestamp_type=pa.timestamp("ms", "America/New_York"),\n    time_of_day_type=pa.time32("ms"),\n)\nrecord_batch = protarrow.messages_to_record_batch(my_protos, MyProto, config)\n```\n\n# Type Mapping\n\n## Native Types\n\n| Proto    | Pyarrow                 | Note         |\n|----------|-------------------------|--------------|\n| bool     | bool_                   |              |\n| bytes    | binary                  |              |\n| double   | float64                 |              |\n| enum     | **int32**/string/binary | configurable |\n| fixed32  | int32                   |              |\n| fixed64  | int64                   |              |\n| float    | float32                 |              |\n| int32    | int32                   |              |\n| int64    | int64                   |              |\n| message  | struct                  |              |\n| sfixed32 | int32                   |              |\n| sfixed64 | int64                   |              |\n| sint32   | int32                   |              |\n| sint64   | int64                   |              |\n| string   | string                  |              |\n| uint32   | uint32                  |              |\n| uint64   | uint64                  |              |\n\n## Other types\n\n\n| Proto                       | Pyarrow                | Note                               |\n|-----------------------------|------------------------|------------------------------------|\n| repeated                    | list_                  |                                    |\n| map                         | map_                   |                                    |\n| google.protobuf.BoolValue   | bool_                  |                                    |\n| google.protobuf.BytesValue  | binary                 |                                    |\n| google.protobuf.DoubleValue | float64                |                                    |\n| google.protobuf.FloatValue  | float32                |                                    |\n| google.protobuf.Int32Value  | int32                  |                                    |\n| google.protobuf.Int64Value  | int64                  |                                    |\n| google.protobuf.StringValue | string                 |                                    |\n| google.protobuf.Timestamp   | timestamp("ns", "UTC") | Unit and timezone are configurable |\n| google.protobuf.UInt32Value | uint32                 |                                    |\n| google.protobuf.UInt64Value | uint64                 |                                    |\n| google.type.Date            | date32()               |                                    |\n| google.type.TimeOfDay       | **time64**/time32      | Unit and type are configurable     |\n\n## Nullability\n\n* Top level native field, list and maps are marked as non-nullable.\n* Any nested message and their children are nullable\n\n# Development\n\n## Set up\n\n```shell\npython3 -m venv --clear venv\nsource venv/bin/activate\npoetry self add "poetry-dynamic-versioning[plugin]"\npoetry install\npython ./scripts/protoc.py\npre-commit install\n```\n\n## Testing\n\nThis library relies on property based testing. \nTests convert randomly generated data from protobuf to arrow and back, making sure the end result is the same as the input.\n\n```shell\ncoverage run --branch --include "*/protarrow/*" -m pytest tests\ncoverage report\n```\n',
    'author': '0x26res',
    'author_email': '0x26res@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tradewelltech/protarrow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
