# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['acycling_digraph_problem']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.2,<4.0.0', 'networkx>=2.8.8,<3.0.0']

entry_points = \
{'console_scripts': ['acycling-digraph-problem = '
                     'acycling_digraph_problem:main']}

setup_kwargs = {
    'name': 'acycling-digraph-problem',
    'version': '0.1.4',
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
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
