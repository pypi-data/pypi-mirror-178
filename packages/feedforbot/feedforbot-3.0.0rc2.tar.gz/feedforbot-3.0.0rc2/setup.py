# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['feedforbot', 'feedforbot.core']

package_data = \
{'': ['*']}

install_requires = \
['aiocron>=1.8,<2.0',
 'aiofiles>=22.1.0,<23.0.0',
 'beautifulsoup4>=4.11.1,<5.0.0',
 'click>=8.1.3,<9.0.0',
 'feedparser>=6.0.10,<7.0.0',
 'httpx>=0.23.1,<0.24.0',
 'jinja2>=3.1.2,<4.0.0',
 'orjson>=3.8.2,<4.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'pyyaml>=6.0,<7.0']

setup_kwargs = {
    'name': 'feedforbot',
    'version': '3.0.0rc2',
    'description': 'Forward links from RSS/Atom feeds to messengers',
    'long_description': 'FeedForBot\n==========\n\n[![PyPI](https://img.shields.io/pypi/v/feedforbot.svg)](https://pypi.python.org/pypi/feedforbot)\n[![PyPI](https://img.shields.io/pypi/dm/feedforbot.svg)](https://pypi.python.org/pypi/feedforbot)\n\nForward links from RSS/Atom feeds to messengers\n',
    'author': 'Aleksandr Shpak',
    'author_email': 'shpaker@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/shpaker/feedforbot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
