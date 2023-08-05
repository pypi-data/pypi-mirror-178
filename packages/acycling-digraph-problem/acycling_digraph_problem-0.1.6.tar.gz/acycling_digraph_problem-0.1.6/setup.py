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
                     'acycling_digraph_problem.main:main']}

setup_kwargs = {
    'name': 'acycling-digraph-problem',
    'version': '0.1.6',
    'description': '',
    'long_description': '# acycling digraph problem\n\n## install\n\n```bash\npip install acycling-digraph-problem\n```\n\n## usage\n\n```bash\nusage: main.py [-h] [--show SHOW] file_path\n\npositional arguments:\nfile_path    path to input file\n\noptions:\n-h, --help   show this help message and exit\n--show SHOW  show graph (default: False)\n```',
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
