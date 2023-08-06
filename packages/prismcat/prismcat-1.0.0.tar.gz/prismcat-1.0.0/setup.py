# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prismcat']

package_data = \
{'': ['*']}

install_requires = \
['ansi2html>=1.8.0,<2.0.0']

entry_points = \
{'console_scripts': ['prism = prismcat.prismcat:cli']}

setup_kwargs = {
    'name': 'prismcat',
    'version': '1.0.0',
    'description': 'parse logs and make pretty colors',
    'long_description': '',
    'author': 'Tyler F. Carr',
    'author_email': 'tcarwash@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
