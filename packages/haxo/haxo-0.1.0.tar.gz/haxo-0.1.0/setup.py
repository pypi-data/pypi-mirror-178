# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['haxo']

package_data = \
{'': ['*']}

install_requires = \
['anyio>=3.6.2,<4.0.0',
 'asyncpg>=0.27.0,<0.28.0',
 'prompt-toolkit>=3.0.33,<4.0.0',
 'pyfiglet>=0.8.post1,<0.9',
 'rich>=12.6.0,<13.0.0',
 'tabulate>=0.9.0,<0.10.0',
 'typer[all]>=0.7.0,<0.8.0',
 'yarl>=1.8.1,<2.0.0']

entry_points = \
{'console_scripts': ['haxo = haxo.console:run']}

setup_kwargs = {
    'name': 'haxo',
    'version': '0.1.0',
    'description': 'A powerful and yet simple PostgreSQL REPL.',
    'long_description': None,
    'author': 'NulX-Studios',
    'author_email': 'nulxstudios@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
