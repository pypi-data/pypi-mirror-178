# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tg_login']

package_data = \
{'': ['*']}

install_requires = \
['Telethon>=1.25.1,<2.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['tg-login = tg_login.cli:app']}

setup_kwargs = {
    'name': 'tg-login',
    'version': '0.0.4',
    'description': 'A command line tool to login into Telegram with user or bot accounts.',
    'long_description': '# tg-login\n\nA command line tool to login into Telegram with user or bot accounts and generate session string.\n\n## Installation\n\n```shell\npip install tg-login\n```\n\n## Usage\n\n```shell\nUsage: tg-login [OPTIONS]\n\n  A command line tool to login into Telegram with user or bot accounts.\n\nOptions:\n  --API_ID INTEGER  API ID obtained from my.telegram.org  [env var: API_ID;\n                    required]\n\n  --API_HASH TEXT   API HASH obtained from my.telegram.org  [env var:\n                    API_HASH; required]\n\n  -v, --version     Show version and exit.\n  --help            Show this message and exit.\n```\n\n## Repl\n\nYou may run this `tg-login` online by using this repl.\n\n[![run on repl](https://docs.replit.com/images/repls/run-on-replit.svg)](https://replit.com/@aahnik/tg-login)\n\nNote:\n\n- A python virtual environment is created before execution and deleted post execution.\n- All sensitive user input is hidden.\n- The session string is not printed on screen, but sent to user.\n',
    'author': 'aahnik',
    'author_email': 'daw@aahnik.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/aahnik/tg-login',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
