# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thingtalk',
 'thingtalk.domains',
 'thingtalk.models',
 'thingtalk.routers',
 'thingtalk.toolkits']

package_data = \
{'': ['*']}

install_requires = \
['async-cron>=1.6.2,<2.0.0',
 'email_validator>=1.1.1,<2.0.0',
 'fastapi>=0.87,<0.88',
 'ifaddr>=0.2.0,<0.3.0',
 'jsonschema>=4.17.0,<5.0.0',
 'loguru>=0.6.0,<0.7.0',
 'orjson>=3.8.1,<4.0.0',
 'pyee>=9.0.0,<10.0.0',
 'uvicorn[standard]>=0.20.0,<0.21.0',
 'zeroconf>=0.39.0,<0.40.0']

extras_require = \
{':python_version >= "3.7" and python_version < "3.8"': ['cached-property>=1.5,<2.0'],
 'docs': ['mkdocs-material>=8.5.0,<9.0.0']}

setup_kwargs = {
    'name': 'thingtalk',
    'version': '0.8.2',
    'description': 'Web of Things framework, high performance, easy to learn, fast to code, ready for production',
    'long_description': '<h1 align="center">Project thingTalk</h1>\n\n<h2 align="center">Thing as a Service</h2>\n\n[![pypi-v](https://img.shields.io/pypi/v/thingtalk.svg)](https://pypi.python.org/pypi/thingtalk)\n[![python](https://img.shields.io/pypi/pyversions/thingtalk.svg)](https://github.com/hidaris/thingtalk)\n\n## What is `thingTalk`?\n`thingTalk` is a web of things implementation, currently supporting a dialect protocol called webthings.\n\n## Project Vision:\nTo provide a communication layer for spatial computing, and make iot interoperable with xr.\n\n### The key features are:\n* Layered design -- Provide services such as rule engines on top of the core protocol layer.\n* Scalability -- Can be based on MQTT to achieve distributed deployment.\n* Standards-based -- Compatibility with community standards[WoT].\n* Fast: Very high performance, on par with NodeJS and Go (thanks to FastAPI).\n* Robust: Get production-ready code. With automatic interactive documentation.\n* Fast to code: Increase the speed to develop features by about 200% to 300%. *\n\n## Installation\nthingtalk can be installed via pip, as such:\n\n`$ pip install thingtalk`\n',
    'author': 'hidaris',
    'author_email': 'zuocool@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/hidaris/thingtalk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
