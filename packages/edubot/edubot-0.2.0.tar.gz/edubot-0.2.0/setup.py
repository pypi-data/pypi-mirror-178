# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['edubot']

package_data = \
{'': ['*']}

install_requires = \
['openai>=0.25.0,<0.26.0', 'sqlalchemy[mypy]>=1.4.44,<1.5.0']

setup_kwargs = {
    'name': 'edubot',
    'version': '0.2.0',
    'description': '',
    'long_description': '# Edubot\n\n## Dev environment quickstart\n1. Install [Poetry](https://python-poetry.org/docs/)\n1. Initialise the env: `poetry install`\n1. Activate the env: `poetry shell`\n1. Install pre-commit hooks: `pre-commit install`\n',
    'author': 'exciteabletom',
    'author_email': 'tom@digitalnook.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
