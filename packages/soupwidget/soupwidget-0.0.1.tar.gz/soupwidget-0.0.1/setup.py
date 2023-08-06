# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['soupwidget']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0']

setup_kwargs = {
    'name': 'soupwidget',
    'version': '0.0.1',
    'description': 'soupwidget',
    'long_description': '',
    'author': 'Thiago César',
    'author_email': 'thiago.cesarmn@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
