# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['msb_core',
 'msb_core.api',
 'msb_core.api.services',
 'msb_core.api.views',
 'msb_core.api.wrappers',
 'msb_core.auth',
 'msb_core.classes',
 'msb_core.conf',
 'msb_core.conf.env',
 'msb_core.conf.logging',
 'msb_core.db',
 'msb_core.db.models',
 'msb_core.exceptions',
 'msb_core.testing',
 'msb_core.utils',
 'msb_core.utils.devtools',
 'msb_core.utils.file',
 'msb_core.utils.file.core',
 'msb_core.wrappers',
 'msb_core.wrappers.datetime',
 'msb_core.wrappers.encryption',
 'msb_core.wrappers.validation',
 'msb_ext']

package_data = \
{'': ['*']}

install_requires = \
['cerberus>=1.3.4,<2.0.0',
 'cffi>=1.15.1,<2.0.0',
 'cryptography>=38.0.3,<39.0.0',
 'django>=4.1.3,<5.0.0',
 'djangorestframework-simplejwt==5.1.0',
 'djangorestframework==3.13.1',
 'pandas>=1.5.1,<2.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'requests>=2.28.1,<3.0.0',
 'xhtml2pdf>=0.2.8,<0.3.0']

setup_kwargs = {
    'name': 'hrin-msb',
    'version': '0.1.3',
    'description': '',
    'long_description': '# hrin-msb\n\n## Pre-requisites for setup\n1. `pip install poetry`\n\n## How To Build\n\n1. `poetry build`\n2. `poetry config http-basic.pypi __token__ <access-token>`\n3. `poetry publish`\n\n\n# Change Log\n ### Version 0.1.1\n\n ### Version 0.1.2\n\n ### Version 0.1.3\n\n1.  Default serializer added to ApiView\n2. fixed incorrect import in _validators.py\n3. fixed msb_database_router\n4. fixed Config.is_local_env() not working\n5. moved devscripts -> utils/devtools\n6. File Utils Added to utils/files\n7. "app_label" removed from "TestConfig" & "ApiTest" Classes\n8. Fixed Bug : \'LoggingModelManager\' object has no attribute \'_queryset_class\'\n9. Fixed : Logging Model not showing any records\n10. Fixed : str method for base model, & removed current_timestamp method from base model',
    'author': 'Prakash Mishra',
    'author_email': 'prakash.mishra@intimetec.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
