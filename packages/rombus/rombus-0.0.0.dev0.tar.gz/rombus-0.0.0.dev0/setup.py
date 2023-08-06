# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'python'}

packages = \
['rombus', 'rombus.tests']

package_data = \
{'': ['*']}

extras_require = \
{'docs': ['Sphinx==5.3.0',
          'sphinx-rtd-theme==1.0.0',
          'myst-parser>=0.18.1,<0.19.0']}

setup_kwargs = {
    'name': 'rombus',
    'version': '0.0.0.dev0',
    'description': 'Reduced order modeling for the masses',
    'long_description': 'Rombus\n======\n\nThis project is being developed in the course of delivering the RSmith_2022B ADACS Merit Allocation Program project.\n',
    'author': 'Gregory Poole',
    'author_email': 'gbpoole@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ADACS-Australia/rombus',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.11',
}


setup(**setup_kwargs)
