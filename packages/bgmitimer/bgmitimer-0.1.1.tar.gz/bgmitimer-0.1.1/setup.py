# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bgmitimer']

package_data = \
{'': ['*']}

install_requires = \
['dacite>=1.6.0,<2.0.0', 'fire>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['bgmitimer = bgmitimer:main']}

setup_kwargs = {
    'name': 'bgmitimer',
    'version': '0.1.1',
    'description': 'write down your work time.',
    'long_description': "# Why It's name is BgmiTimer?\n\nBecause I want to watch anime between two working time.",
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
