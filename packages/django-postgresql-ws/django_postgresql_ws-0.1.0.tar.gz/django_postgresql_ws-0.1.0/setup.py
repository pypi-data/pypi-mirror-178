# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_postgresql_ws']

package_data = \
{'': ['*']}

install_requires = \
['asgiref>=3.5.2,<4.0.0', 'django>=4.1.3,<5.0.0', 'pgwasm>=0.2.1,<0.3.0']

setup_kwargs = {
    'name': 'django-postgresql-ws',
    'version': '0.1.0',
    'description': 'Django PostgreSQL backend proxied over WebSockets (for WASM)',
    'long_description': 'django-postgresql-ws\n--------------------\n\n`django-postgresql-ws` is an alternative PostgreSQL backend for Django \nproxied over WebSockets. It will only work when configured to run against a \nWebSockets proxy that is then communicating with the PostgreSQL server. \nwebsockify is the standard WebSockets proxy service it is tested against.\n\nThe purpose of this backend is to allow a Django application to run against \na PostgreSQL server in a WebAssembly (Pyodide) environment, where native \nsockets are \nnot allowed but WebSockets are. The WebSocket communication is handled by \nthe pgwasm library, which itself switches between using a the native \nwebsockets libray when being run in a native environment, and using the \nJS-proxied interface when run under Pyodide.\n\nThis backend is based on a copy of the PostgreSQL backend that \nships with Django 4.1 with updates made to use `pgwasm` instead of \n`psycopg2`. Note that while Django does not natively support async in its \nimplementation of its ORM, the database backend needs to be async in order \nto communicate over WebSockets in Pyodide, since the JS interface receives \nWebSockets messages via callbacks. The `async_to_sync` method provided by \n`asgiref` properly handle running the async methods in the proper event loop.\n',
    'author': 'dek',
    'author_email': 'dek@substructure.one',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/SubstructureOne/django-postgresql-ws',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
