# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sophia_doc', 'sophia_doc.builders']

package_data = \
{'': ['*']}

install_requires = \
['docstring-parser>=0.15,<0.16']

entry_points = \
{'console_scripts': ['sophia-doc = sophia_doc.__main__:cli']}

setup_kwargs = {
    'name': 'sophia-doc',
    'version': '0.1.0',
    'description': 'A python package to automatically generate API documents for Python modules.',
    'long_description': 'None',
    'author': 'st1020',
    'author_email': 'stone_1020@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
