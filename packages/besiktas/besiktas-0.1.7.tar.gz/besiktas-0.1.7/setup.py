# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['besiktas']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'requests>=2.28.1,<3.0.0',
 'rich>=12.6.0,<13.0.0']

entry_points = \
{'besiktas.plugin': ['besiktas = besiktas.cli:main'],
 'console_scripts': ['besiktas = besiktas.cli:main']}

setup_kwargs = {
    'name': 'besiktas',
    'version': '0.1.7',
    'description': 'besiktas cli!',
    'long_description': '# Besiktas\n\nBesiktas CLI!\n\n## Installation\n\n```shell\n$ pip install besiktas\n```\n\n## Usage\nMain Page\n```shell summary\n$ besiktas\n```\nList of Players\n```shell footballers\n$ besiktas -kadro\n```\nList of Top Scorers\n```shell footballers\n$ besiktas -stats\n```\n\n',
    'author': 'uygar',
    'author_email': 'osmanuygar@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/osmanuygar/besiktas',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
