# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['obsigit']

package_data = \
{'': ['*']}

install_requires = \
['dacite>=1.6.0,<2.0.0', 'fire>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['obsigit = obsigit:main']}

setup_kwargs = {
    'name': 'obsigit',
    'version': '0.1.1',
    'description': 'use git to manage notes in obsidian.',
    'long_description': "# Why not use obsidian-git plugin?\n\nIt's different to understand. So I make this script.",
    'author': 'aoout',
    'author_email': 'wuz66280@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
