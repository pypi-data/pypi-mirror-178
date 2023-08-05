# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mesh_sandbox',
 'mesh_sandbox.common',
 'mesh_sandbox.handlers',
 'mesh_sandbox.models',
 'mesh_sandbox.routers',
 'mesh_sandbox.store',
 'mesh_sandbox.tests',
 'mesh_sandbox.views']

package_data = \
{'': ['*'], 'mesh_sandbox.store': ['data/*']}

install_requires = \
['cryptography>=38.0.3,<39.0.0',
 'fastapi>=0.75.0,<0.76.0',
 'gunicorn>=20.1.0,<21.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'types-python-dateutil>=2.8.9,<3.0.0',
 'uvicorn>=0.15.0,<0.16.0']

setup_kwargs = {
    'name': 'mesh-sandbox',
    'version': '0.1.0',
    'description': '',
    'long_description': 'None',
    'author': 'spinecore',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
