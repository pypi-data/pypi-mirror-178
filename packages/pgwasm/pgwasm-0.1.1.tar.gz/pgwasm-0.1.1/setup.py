# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pgwasm']

package_data = \
{'': ['*']}

install_requires = \
['pytest-asyncio>=0.20.2,<0.21.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'scramp>=1.4.4,<2.0.0',
 'wasmsockets>=0.1.3,<0.2.0']

setup_kwargs = {
    'name': 'pgwasm',
    'version': '0.1.1',
    'description': 'PostgreSQL interface for WebAssembly over WebSockets',
    'long_description': 'pgwasm\n======\n\npgwasm is a Python interface to PostgreSQL proxied over WebSockets for use in\nWebAssembly (specifically using Pyodide). It is based on pg8000 and uses\nwasmsockets for communication.\n\nwasmsockets handles the proxying of WebSocket calls to the Javascript \ninterface when it detects it is being run in a WebAssembly environment. When \nrun in a native Python environment, it instead uses the websockets package. \nThis allows pgwasm to be tested in a native environment. However in both \ncases, since all network traffic is proxied over WebSockets, a WebSocket \nproxy is also required for the Postgres server; it cannot connect to a \nPostgreSQL server directly. The websockify package is convenient for \nimplementing this proxy to PostgreSQL.\n',
    'author': 'dek',
    'author_email': 'dek@substructure.one',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/SubstructureOne/pgwasm1',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
