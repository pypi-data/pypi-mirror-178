# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aisci']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23.5,<2.0.0',
 'pandas>=1.5.2,<2.0.0',
 'python-dotenv>=0.19.0,<0.20.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['start = aisci.main:app', 'test = aisci.main:test']}

setup_kwargs = {
    'name': 'aisci',
    'version': '0.1.0',
    'description': '',
    'long_description': 'None',
    'author': 'Freeman Long',
    'author_email': 'goldyard@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
