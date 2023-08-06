# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cpunk_mongo']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=7.2.0,<8.0.0']

setup_kwargs = {
    'name': 'cpunk-mongo',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'matfonseca',
    'author_email': 'mfonseca@fi.uba.ar',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
