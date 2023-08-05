# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['taa']

package_data = \
{'': ['*']}

install_requires = \
['allure-pytest>=2.12.0,<3.0.0',
 'colorlog>=6.7.0,<7.0.0',
 'pyyaml>=6.0,<7.0',
 'sqlalchemy>=1.4.44,<2.0.0',
 'texttable>=1.6.7,<2.0.0']

entry_points = \
{'console_scripts': ['taa = taa.cli:main'],
 'pytest11': ['taa = taa.plugin:Plugin']}

setup_kwargs = {
    'name': 'taa',
    'version': '0.1.1',
    'description': '接口自动化工具',
    'long_description': 'try-api-auto\n尝试编写接口自动化-脚手架',
    'author': '雪峰365',
    'author_email': '120158568@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/xuefeng365/api-autotest.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
