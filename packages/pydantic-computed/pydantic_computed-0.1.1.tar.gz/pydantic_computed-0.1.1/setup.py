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
    'version': '0.1.1',
    'description': 'A new decorator for pydantic allowing you to define dynamic fields that are computed from other properties',
    'long_description': '# pydantic-computed\nA new decorator for pydantic allowing you to define dynamic fields that are computed from other properties.\n\n## Installation\n\nInstall the package by running\n```bash\npip install pydantic_computed\n```\n\n## Examples and use cases\n\n### A computed integer property\n```python\nfrom pydantic import BaseModel\nfrom pydantic_computed import Computed, computed\n\nclass ExampleModel(BaseModel):\n    a: int\n    b: int\n    c: Computed[int]\n\n    @computed(\'c\')\n    def calculate_c(a: int, **kwargs):\n        return a + 1\n\nmodel = ExampleModel(a=1, b=2)\nprint(model.c) # Outputs 2\n```\n\n### Multiple properties as parameters\n\n```python\nfrom pydantic import BaseModel\nfrom pydantic_computed import Computed, computed\n\nclass ExampleModel(BaseModel):\n    a: int\n    b: int\n    c: Computed[int]\n\n    @computed(\'c\')\n    def calculate_c(a: int, b: int):\n        return a + 1\n\nmodel = ExampleModel(a=1, b=2)\nprint(model.c) # Outputs 2\n```\n\nSince all properties are passed as **kwargs to calculate_c, we can use the property names for the parameters\n\n### Automatic type conversion\n\n```python\nfrom pydantic import BaseModel\nfrom pydantic_computed import Computed, computed\n\nclass ExampleModel(BaseModel):\n    a: int\n    b: int\n    c: Computed[str]\n\n    @computed(\'c\')\n    def calculate_c(a: int, b: int):\n        return a + b\n\nmodel = ExampleModel(a=1, b=2)\nprint(model.c) # Outputs \'3\' as string\n```\n\nAutomatic type conversion happens for the returned value\n\n### Complex types\n\nSuppose you set up a FastAPI application where you have users and orders stored in a database.\nAll Models in the database have an automatically generated id.\nNow you want to be able to dynamically generate links to those objects.\nE.g. the user with id=3 is accessible on the endpoint http://my-api/users/3\nInstead of storing those links in the database you can simply generate them with the computed decorator.\nexample: \n\n```python\nfrom pydantic import BaseModel, Field\nfrom pydantic_computed import Computed, computed\n\nclass Link(BaseModel):\n    href: str\n    method: str\n\nclass SchemaLinked(BaseModel):\n    id: int\n    base_url: str\n    link: Computed[Link]\n    @computed(\'link\')\n    def compute_link( id: int, base_url: str):        \n        return Link(href=f\'{base_url}/{id}\', method=\'GET\')\n\nclass User(SchemaLinked):\n    base_url: str = Field(\'/users\', exclude=True)\n    username: str\n\nclass Order(SchemaLinked):\n    base_url: str = Field(\'/orders\', exclude=True)\n    user: User\n\nuser = User(id=3, username=\'exampleuser\') \nuser.json()\n"""\n{\n    id: 3,\n    username: "exampleuser",\n    link: {\n        href: "/users/3",\n        method: "GET"\n    }\n}\n"""\norder = Order(id=2, user=user)\norder.json()\n"""\n{\n    id: 2,\n    link: {\n        href: "/orders/2",\n        method: "GET"\n    },\n    user: {\n        id: 3,\n        username: "exampleuser",\n        link: {\n            href: "/users/3",\n            method: "GET"\n        }\n    }\n}\n"""\n``` \n',
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
