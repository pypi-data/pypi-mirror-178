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
    'version': '0.1.3',
    'description': 'NHSDigital mesh sandbox, a locally testable version of the MESH api',
    'long_description': 'MESH Sandbox\n===========\n\nMESH sandbox for local testing of [NHS Digital\'s MESH API](https://digital.nhs.uk/developer/api-catalogue/message-exchange-for-social-care-and-health-api).\n\nInstallation\n------------\n\n\nExample use\n-----------\n\npip\n---\n```bash\npip install mesh-sandbox\nSTORE_MODE=file FILE_STORE_DIR=/tmp/mesh uvicorn mesh_sandbox.api:app --reload --port 8700 --workers=1\ncurl http://localhost:8700/health\n```\n\ndocker compose\n--------------\n```yaml\nversion: \'3.9\'\n\n\nservices:\n\n  mesh_sandbox:\n    build: \n      context: https://github.com/NHSDigital/mesh-sandbox.git#develop\n    ports:\n      - "8700:80"\n    deploy:\n      restart_policy:\n        condition: on-failure\n        max_attempts: 3\n    healthcheck:\n      test: curl -sf http://localhost:80/health || exit 1\n      interval: 3s\n      timeout: 10s\n    environment:\n      - SHARED_KEY=TestKey\n    volumes:\n      # mount a different mailboxes.jsonl to pre created mailboxes\n      - ./src/mesh_sandbox/store/data/mailboxes.jsonl:/app/mesh_sandbox/store/data/mailboxes.jsonl:ro\n\n```\n\nGuidance for contributors\n-------------------------\nthis project uses\n- python 3.9\n- java coretto11\n- poetry > 1.2\n\nSetup\n-----\nusing asdf\n[install asdf](https://asdf-vm.com/guide/getting-started.html#_3-install-asdf)\n\nget the required plugins\n```bash\nadsf plugin install python\nadsf plugin install java\nadsf plugin install poetry\n```\n\ninstall the tools\n```bash\ncd <project_dir>\nasdf install\n```\n\ninstall the dependencies\n```bash\nmake install\n```',
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
