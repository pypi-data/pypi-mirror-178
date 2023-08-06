# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysource_minimize']

package_data = \
{'': ['*']}

install_requires = \
['asttokens>=2.0.8,<3.0.0', 'rich>=12.6.0,<13.0.0']

setup_kwargs = {
    'name': 'pysource-minimize',
    'version': '0.1.0',
    'description': 'find failing section in python source',
    'long_description': '',
    'author': 'Frank Hoffmann',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
