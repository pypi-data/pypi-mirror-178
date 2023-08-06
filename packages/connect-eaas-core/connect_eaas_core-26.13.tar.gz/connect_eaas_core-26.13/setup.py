# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['connect',
 'connect.eaas.core',
 'connect.eaas.core.inject',
 'connect.eaas.core.testing',
 'connect.eaas.core.validation',
 'connect.eaas.core.validation.validators']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'anvil-uplink>=0.4.0,<0.5.0',
 'connect-openapi-client>=25.15',
 'fastapi-utils>=0.2.1,<0.3.0',
 'fastapi>=0.78.0,<0.79.0',
 'logzio-python-handler>=3.1.1,<4.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'pytest11': ['pytest_eaas_core = connect.eaas.core.testing.fixtures']}

setup_kwargs = {
    'name': 'connect-eaas-core',
    'version': '26.13',
    'description': 'Connect Eaas Core',
    'long_description': '',
    'author': 'CloudBlue LLC',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://connect.cloudblue.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
