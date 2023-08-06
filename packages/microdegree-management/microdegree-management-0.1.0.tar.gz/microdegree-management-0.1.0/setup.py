# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['microdegree_management']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'graphviz>=0.20.1,<0.21.0',
 'pydantic-yaml>=0.8.1,<0.9.0',
 'pydantic>=1.10.2,<2.0.0',
 'types-PyYAML>=6.0.12,<7.0.0']

setup_kwargs = {
    'name': 'microdegree-management',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Vincent Nys',
    'author_email': 'vincent.nys@ap.be',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
