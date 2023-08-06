# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['more_polars']

package_data = \
{'': ['*']}

install_requires = \
['composable>=0.5.4', 'polars>=0.14.26']

setup_kwargs = {
    'name': 'more-polars',
    'version': '0.3.0',
    'description': '',
    'long_description': '',
    'author': 'Todd Iverson',
    'author_email': 'Tiverson@winona.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
