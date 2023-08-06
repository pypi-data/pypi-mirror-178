# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qattools']

package_data = \
{'': ['*']}

install_requires = \
['pandas', 'torch', 'torchinfo']

setup_kwargs = {
    'name': 'qattools',
    'version': '0.3.3',
    'description': '',
    'long_description': '',
    'author': 'Richard Hajek',
    'author_email': 'richard.m.hajek@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
