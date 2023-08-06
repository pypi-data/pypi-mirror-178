# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pfatools', 'pfatools.random_person', 'pfatools.utils']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'pfatools',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'msherburne',
    'author_email': 'mathieusherburne@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
