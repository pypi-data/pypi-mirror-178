# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['randomalphabets']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'randomalphabets',
    'version': '0.1.0',
    'description': 'Generate a string of n random alphabets.',
    'long_description': None,
    'author': 'Ashin K Ajay',
    'author_email': 'ashinkajayclt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
