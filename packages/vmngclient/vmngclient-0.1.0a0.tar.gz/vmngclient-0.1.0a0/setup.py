# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vmngclient', 'vmngclient.api', 'vmngclient.tests', 'vmngclient.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'attrs>=21.4.0,<22.0.0',
 'ciscoconfparse>=1.6.40,<2.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'requests>=2.27.1,<3.0.0',
 'tenacity>=8.1.0,<9.0.0']

setup_kwargs = {
    'name': 'vmngclient',
    'version': '0.1.0a0',
    'description': 'Universal vManage API',
    'long_description': '# vManage-client\n[![Python3.8](https://img.shields.io/static/v1?label=Python&logo=Python&color=3776AB&message=3.8)](https://www.python.org/)\n\nvManage client is a package for creating simple and parallel automatic requests via official vManageAPI. It is intended to serve as a multiple session handler (provider, provider as a tenant, tenant). The library is not dependent on environment which is being ran, you just need a connection to any vManage.',
    'author': 'kagorski',
    'author_email': 'kagorski@cisco.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CiscoDevNet/vManage-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
