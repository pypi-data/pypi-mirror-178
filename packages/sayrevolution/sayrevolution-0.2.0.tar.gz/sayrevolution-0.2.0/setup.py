# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sayrevolution']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['revolution = sayrevolution:say_it']}

setup_kwargs = {
    'name': 'sayrevolution',
    'version': '0.2.0',
    'description': 'It says revolution',
    'long_description': None,
    'author': 'Sam Lavigne',
    'author_email': 'splavigne@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
