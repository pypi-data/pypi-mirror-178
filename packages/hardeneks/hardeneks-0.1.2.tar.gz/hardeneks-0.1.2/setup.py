# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hardeneks',
 'hardeneks.cluster_wide',
 'hardeneks.cluster_wide.reliability',
 'hardeneks.cluster_wide.security',
 'hardeneks.namespace_based',
 'hardeneks.namespace_based.reliability',
 'hardeneks.namespace_based.security']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.26.2,<2.0.0',
 'kubernetes>=25.3.0,<26.0.0',
 'pre-commit>=2.20.0,<3.0.0',
 'typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['hardeneks = hardeneks:app']}

setup_kwargs = {
    'name': 'hardeneks',
    'version': '0.1.2',
    'description': '',
    'long_description': '# Hardeneks\n\n[![PyPI version](https://badge.fury.io/py/hardeneks.svg)](https://badge.fury.io/py/hardeneks)\n[![PyPI Supported Python Versions](https://img.shields.io/pypi/pyversions/hardeneks.svg)](https://pypi.python.org/pypi/hardeneks/)\n[![Python package](https://github.com/dorukozturk/hardeneks/actions/workflows/ci.yaml/badge.svg)](https://github.com/dorukozturk/hardeneks/actions/workflows/ci.yaml)\n',
    'author': 'Doruk Ozturk',
    'author_email': 'dozturk@amazon.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
