# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_demo']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0']

setup_kwargs = {
    'name': 'poetry-demo-taurus',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': '袁郑',
    'author_email': 'yzheng@epoint.com.cn',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
