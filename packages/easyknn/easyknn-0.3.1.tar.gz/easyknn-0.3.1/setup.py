# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['easyknn']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'easyknn',
    'version': '0.3.1',
    'description': 'Easy nearest neighbors using Annoy or SKLearn',
    'long_description': None,
    'author': 'Sanjaya Subedi',
    'author_email': 'jangedoo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
