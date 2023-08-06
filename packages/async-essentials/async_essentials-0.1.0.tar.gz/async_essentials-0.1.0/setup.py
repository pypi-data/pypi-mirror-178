# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['async_essentials', 'async_essentials.endpoints', 'async_essentials.models']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.1,<0.24.0']

setup_kwargs = {
    'name': 'async-essentials',
    'version': '0.1.0',
    'description': 'An asynchronous python client for the proof point essentials API',
    'long_description': 'None',
    'author': 'symonk',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
