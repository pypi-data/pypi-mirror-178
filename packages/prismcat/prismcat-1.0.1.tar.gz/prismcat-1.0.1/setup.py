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
    'version': '1.0.1',
    'description': 'parse logs and make pretty colors',
    'long_description': "# PrismCat\n\n## Explanation\nPrismCat reads a file (or stdin) and highlights lines based on regex supplied in arguments. \n\nColors follow the rainbow in priority e.g. (Error)>Red>Yellow>Green>Blue>Purple and are specified as arguments with their initial letter: -e -r -y -g -b -p, each taking a quoted regular expression as input. \n\nPrismCat can output to stdin, or to an html file (using the -o option) for future reference retaining the coloring. \n\nthe -a flag eliminates all lines that aren't currently highlighted, filtering output to only the important lines. \n\n## Future\nEventually, PrismCat should be a full drop-in replacement for cat with the additional features provided in the current version",
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
