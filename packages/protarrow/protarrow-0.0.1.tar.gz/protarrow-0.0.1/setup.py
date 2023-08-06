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
    'version': '0.0.1',
    'description': 'Convert from protobuf to arrow and back',
    'long_description': '[![PyPI Version][pypi-image]][pypi-url]\n[![][versions-image]][versions-url]\n[![][stars-image]][stars-url]\n[![codecov](https://codecov.io/gh/0x26res/protarrow/branch/master/graph/badge.svg?token=XMFH27IL70)](https://codecov.io/gh/0x26res/protarrow)\n[![Build Status][build-image]][build-url]\n[![Documentation][doc-image]][doc-url]\n\n\n# Protarrow\n\nA python library for converting from protobuf to arrow and back \n\n# Installation\n\n```shell\npip install protarrow\n```\n\n# Usage\n\nSee the [documentation](https://protarrow.readthedocs.io/en/latest/)\n\n\n<!-- Badges: -->\n\n[pypi-image]: https://img.shields.io/pypi/v/protarrow\n[pypi-url]: https://pypi.org/project/protarrow/\n[build-image]: https://github.com/tradewelltech/protarrow/actions/workflows/build.yaml/badge.svg\n[build-url]: https://github.com/tradewelltech/protarrow/actions/workflows/build.yaml\n[stars-image]: https://img.shields.io/github/stars/tradewelltech/protarrow\n[stars-url]: https://github.com/tradewelltech/protarrow\n[versions-image]: https://img.shields.io/pypi/pyversions/protarrow\n[versions-url]: https://pypi.org/project/protarrow/\n[doc-image]: https://readthedocs.org/projects/protarrow/badge/?version=latest\n[doc-url]: https://protarrow.readthedocs.io/en/latest/?badge=latest\n',
    'author': '0x26res',
    'author_email': '0x26res@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tradewelltech/protarrow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
