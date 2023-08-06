# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['erkr_semver_test2']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.2.2,<3.0.0', 'fastapi>=0.85.1,<0.86.0']

setup_kwargs = {
    'name': 'erkr-semver-test2',
    'version': '2.0.0',
    'description': 'This is the decription',
    'long_description': 'This is a readme',
    'author': 'Eran Kricheli',
    'author_email': 'eran.kricheli@frontegg.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
