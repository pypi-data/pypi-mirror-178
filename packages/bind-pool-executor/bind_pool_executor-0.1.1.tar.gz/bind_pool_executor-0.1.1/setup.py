# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bind_pool_executor']

package_data = \
{'': ['*']}

install_requires = \
['importlib_metadata>=3.4.0,<4.0.0']

setup_kwargs = {
    'name': 'bind-pool-executor',
    'version': '0.1.1',
    'description': '捆绑池处理，在一个工作执行完开始另一个工作的执行',
    'long_description': '# bind-pool-executor\n\n\n[![PyPI version](https://badge.fury.io/py/bind-pool-executor.svg)](https://badge.fury.io/py/bind-pool-executor)\n![versions](https://img.shields.io/pypi/pyversions/bind-pool-executor.svg)\n[![GitHub license](https://img.shields.io/github/license/mgancita/bind-pool-executor.svg)](https://github.com/mgancita/bind-pool-executor/blob/main/LICENSE)\n\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n\n捆绑池处理，在一个工作执行完开始另一个工作的执行\n\n\n- 开源许可: MIT\n- 文档: https://llango.github.io/bind-pool-executor.\n\n\n## 特征\n\n* TODO\n\n## 制作\n\n\n该包使用 [Cookiecutter](https://github.com/audreyr/cookiecutter) 和 [`llango/cookiecutter-mkdoc-shapackage`](https://github.com/llango/cookiecutter-mkdoc-shapackage/) 项目模版创建。\n',
    'author': 'Rontomai',
    'author_email': 'rontomai@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/llango/bind-pool-executor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
