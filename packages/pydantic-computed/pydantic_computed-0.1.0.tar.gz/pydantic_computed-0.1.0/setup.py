# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydantic_computed']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.2,<2.0.0', 'setuptools>=65.6.3,<66.0.0']

setup_kwargs = {
    'name': 'pydantic-computed',
    'version': '0.1.0',
    'description': 'A new decorator for pydantic allowing you to define dynamic fields that are computed from other properties',
    'long_description': '# pydantic-computed\nA new decorator for pydantic allowing you to define dynamic fields that are computed from other properties.\n',
    'author': 'Jakob Leibetseder',
    'author_email': 'leibetsederjakob@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Maydmor/pydantic-computed',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
