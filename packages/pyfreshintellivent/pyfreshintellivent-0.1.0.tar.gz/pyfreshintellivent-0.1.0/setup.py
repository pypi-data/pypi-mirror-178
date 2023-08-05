# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyfreshintellivent']

package_data = \
{'': ['*']}

install_requires = \
['bleak==0.19.4']

setup_kwargs = {
    'name': 'pyfreshintellivent',
    'version': '0.1.0',
    'description': 'Manage Fresh Intellivent Sky bathroom ventilation fan',
    'long_description': '# PyFreshSky\nPython interface for Fresh Intellivent Sky bathroom Fan using Bluetooth Low Energy.\n\n## Documentation\nCheck out the [Characteristics file](characteristics.md) file to read more about known characteristics.\n',
    'author': 'Ståle Storø Hauknes',
    'author_email': 'walnut-caprice.04@icloud.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/LaStrada/pyfreshintellivent',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
