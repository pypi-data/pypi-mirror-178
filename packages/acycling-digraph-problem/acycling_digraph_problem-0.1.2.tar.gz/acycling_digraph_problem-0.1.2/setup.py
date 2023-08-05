# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['acycling_digraph_problem']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=2.8.8,<3.0.0']

setup_kwargs = {
    'name': 'acycling-digraph-problem',
    'version': '0.1.2',
    'description': '',
    'long_description': '# acycling digraph problem',
    'author': 'ada0l',
    'author_email': 'andreika.varfolomeev@yandex.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
