# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['picods']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib', 'numpy>=1.23.5,<2.0.0', 'pandas>=1.5.2,<2.0.0']

setup_kwargs = {
    'name': 'picods',
    'version': '0.1.0',
    'description': 'Pico Data Science: A small, personal use case, Data Science library.',
    'long_description': '# pds\n',
    'author': 'Pablo',
    'author_email': 'pablohuggem@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
