# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['google-stubs']

package_data = \
{'': ['*'],
 'google-stubs': ['api/*',
                  'cloud/*',
                  'cloud/location/*',
                  'gapic/metadata/*',
                  'logging/type/*',
                  'longrunning/*',
                  'rpc/*',
                  'rpc/context/*',
                  'type/*']}

install_requires = \
['googleapis-common-protos>=1.56.4',
 'grpc-stubs>=1.24.9',
 'types-protobuf>=3.20.4.2',
 'typing-extensions>=3.10.0']

setup_kwargs = {
    'name': 'googleapis-common-protos-stubs',
    'version': '2.2.0',
    'description': 'Type stubs for googleapis-common-protos',
    'long_description': "# Type stubs for googleapis-common-protos\n[![PyPI version](https://badge.fury.io/py/googleapis-common-protos-stubs.svg)](https://badge.fury.io/py/googleapis-common-protos-stubs)\n\nThis package provides type stubs for the [googleapis-common-protos](https://pypi.org/project/googleapis-common-protos/) package.\n\n**This is in no way affiliated with Google.**\n\nThe stubs were created automatically by [mypy-protobuf](https://github.com/dropbox/mypy-protobuf).\n\nNote that if you're using Mypy you need to use the `--namespace-packages` option as `google` and some of its subpackages are namespace packages.\n\n## Installation\n```shell script\n$ pip install googleapis-common-protos-stubs\n```\n",
    'author': 'Henrik Bruåsdal',
    'author_email': 'henrik.bruasdal@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/henribru/googleapis-common-protos-stubs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
