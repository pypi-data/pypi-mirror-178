# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pubhelper']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'pubhelper',
    'version': '0.0.2',
    'description': '',
    'long_description': '# PubHelper\n\n- [x] 添加 retry_wraps\n- [x] 添加 request_base\n- [x] 添加 rdm_str\n- [x] 添加 md5',
    'author': 'iulmt',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
