# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_stack_utils', 'fastapi_stack_utils.schemas']

package_data = \
{'': ['*']}

install_requires = \
['asgi-correlation-id==3.2.1',
 'fastapi==0.87.0',
 'gunicorn==20.1.0',
 'python-json-logger==2.0.4',
 'pytz==2022.6',
 'sentry-sdk==1.11.1',
 'uvicorn[standard]==0.20.0']

setup_kwargs = {
    'name': 'fastapi-stack-utils',
    'version': '0.7.1',
    'description': 'Utils to extend the FastAPI with logging and exception handlers',
    'long_description': 'None',
    'author': 'Jonas Krüger Svensson',
    'author_email': 'jonas-ks@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
