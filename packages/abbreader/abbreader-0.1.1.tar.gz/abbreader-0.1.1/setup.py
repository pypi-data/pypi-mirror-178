# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['abbreader']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2', 'pendulum>=2.1.2,<3.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'abbreader',
    'version': '0.1.1',
    'description': 'abb reader',
    'long_description': None,
    'author': 'John N',
    'author_email': 'niedrachj@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
