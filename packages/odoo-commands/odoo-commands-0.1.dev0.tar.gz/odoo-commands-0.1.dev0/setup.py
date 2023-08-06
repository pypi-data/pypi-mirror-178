# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['odoo_commands']

package_data = \
{'': ['*']}

install_requires = \
['click-odoo-contrib>=1.15.0,<2.0.0',
 'click_odoo>=1.5.0,<2.0.0',
 'ipython',
 'manifestoo-core>=0.10.2,<0.11.0',
 'networkx<2.7',
 'tomlkit>=0.7.2,<0.8.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['oc = ocli.main:app']}

setup_kwargs = {
    'name': 'odoo-commands',
    'version': '0.1.dev0',
    'description': 'Project description',
    'long_description': None,
    'author': 'Dmitry Voronin',
    'author_email': 'dimka665@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/voronind/ocli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
