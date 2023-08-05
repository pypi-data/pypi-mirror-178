# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['danbi_fastapi']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'danbi-fastapi',
    'version': '0.1.29',
    'description': 'danbi plugin for fastapi',
    'long_description': '# danbi-fastapi\nfastapi plugin based on danbi library\n',
    'author': 'nockchun',
    'author_email': 'nockchun@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nockchun/danbi-fastapi',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
