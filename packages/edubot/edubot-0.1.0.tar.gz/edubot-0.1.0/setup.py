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
    'version': '0.1.0',
    'description': '',
    'long_description': '# Edubot\n',
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
