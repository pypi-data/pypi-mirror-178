# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mfdtool']

package_data = \
{'': ['*']}

install_requires = \
['bitstring>=4.0.1,<5.0.0', 'click>=8.1.3,<9.0.0']

entry_points = \
{'console_scripts': ['mfdtool = mfdtool.tool:cli']}

setup_kwargs = {
    'name': 'mfdtool',
    'version': '0.1.1',
    'description': 'Convert NFC card dumps between Flipper Zero and MFD dumps',
    'long_description': None,
    'author': 'Viktor Stískala',
    'author_email': 'viktor@stiskala.cz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
