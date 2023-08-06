# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flake8_global_variables']

package_data = \
{'': ['*']}

install_requires = \
['flake8>=6.0.0,<7.0.0']

entry_points = \
{'flake8.extension': ['GV4 = flake8_global_variables:GlobalVariablesChecker']}

setup_kwargs = {
    'name': 'flake8-global-variables',
    'version': '0.1.2',
    'description': 'Flake8 plugin to forbid global variables',
    'long_description': '',
    'author': 'pacificus',
    'author_email': 'masterkristall@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/pacifikus/flake8-global-variables',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4.0',
}


setup(**setup_kwargs)
