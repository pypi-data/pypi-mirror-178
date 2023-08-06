# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['constellationpy']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'click-default-group>=1.2.2,<2.0.0',
 'click>=8.0.3,<9.0.0',
 'pandas>=1.3.4,<2.0.0',
 'semantic-version>=2.8.5,<3.0.0',
 'trio-websocket>=0.9.2,<0.10.0',
 'trio>=0.21.0,<0.22.0',
 'urllib3>=1.26.11,<2.0.0']

setup_kwargs = {
    'name': 'constellationpy',
    'version': '0.2.0',
    'description': 'Client Python pour le réseau Constellation.',
    'long_description': 'None',
    'author': 'Julien Jean Malard-Adam',
    'author_email': 'julien.malard@mail.mcgill.ca',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
