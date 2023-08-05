# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quicklook']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.2,<4.0.0',
 'numpy>=1.23.4,<2.0.0',
 'rich>=12.6.0,<13.0.0',
 'typer>=0.7.0,<0.8.0']

setup_kwargs = {
    'name': 'quicklook',
    'version': '1.0.0',
    'description': 'An easy way to view numpy arrays',
    'long_description': '# quicklook\nAn easy way to view numpy arrays.\n\nHere are the [docs](https://samsammurphy.github.io/quicklook/)',
    'author': 'Sam Murphy',
    'author_email': 'samsammurphy@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
