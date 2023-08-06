# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['filpick']

package_data = \
{'': ['*']}

install_requires = \
['dacite>=1.6.0,<2.0.0', 'fire>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['filpick = filpick:main']}

setup_kwargs = {
    'name': 'filpick',
    'version': '0.1.2',
    'description': '',
    'long_description': '',
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
