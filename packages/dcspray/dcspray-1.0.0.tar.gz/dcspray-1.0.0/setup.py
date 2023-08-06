# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dcspray', 'dcspray.util']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.2.0,<10.0.0',
 'dracoon>=1.8.0,<2.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'python-resize-image>=1.1.20,<2.0.0',
 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['dcspray = dcspray.cli:app']}

setup_kwargs = {
    'name': 'dcspray',
    'version': '1.0.0',
    'description': 'DRACOON Sprayer - Branding utility for DRACOON',
    'long_description': 'None',
    'author': 'Octavio Simone',
    'author_email': '70800577+unbekanntes-pferd@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
