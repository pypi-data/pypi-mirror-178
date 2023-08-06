# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qattools']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.5.2,<2.0.0', 'torch>=1.13.0,<2.0.0', 'torchinfo>=1.7.1,<2.0.0']

setup_kwargs = {
    'name': 'qattools',
    'version': '0.2.0',
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
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
