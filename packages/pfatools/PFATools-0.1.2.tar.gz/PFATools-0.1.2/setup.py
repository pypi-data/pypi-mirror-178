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
    'version': '0.1.2',
    'description': 'Collection of tools used for teaching python through API requests and data exploration.',
    'long_description': '# PFATools\nPFATools is a collection of tools used for teaching python through API requests and data exploration. It is written in Python and is available under the MIT license.\n\nYou need Python 3.8 or higher to run PFATools.\n### Contents\n- [PFATools](#pfatools)\n    - [Contents](#contents)\n    - [Installation](#installation)\n    - [API Tools](#api-tools)\n      - [Name Predictions](#name-predictions)\n      - [Random Person](#random-person)\n\n\n\n\n### Installation\nUse pip to pull from the PyPi repository:\n```bash\npip install pfatools\n```\n### API Tools\n#### Name Predictions\nCan predict various things through a single name. Returns the raw JSON response from the API.\n```python\nfrom pfatools import *\nname = "John"\nage_response = age_predictor(name)\ngender_response = gender_predictor(name)\nnationality_response = nationality_predictor(name)\n```\nThe only argument for these functions are ```name```\n\n#### Random Person\nReturns random person data. Returns the raw JSON response from the API.\n```python\nfrom pfatools import *\nperson = randomPerson()\ndata = person.data\n```\n*Arguments:*\n| Argument | Type | Description |\n| --- | --- | --- |\n| amount | int | amount of people to generate. default: 1 (>= 1) |\n| defer | bool | whether to defer the request or not. default: False |\n\nmethod *run_query*\nruns the query and returns the raw JSON response from the API.\n```python\nfrom pfatools import *\nperson = randomPerson(defer=True)\ndata = person.run_query()\n```',
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
