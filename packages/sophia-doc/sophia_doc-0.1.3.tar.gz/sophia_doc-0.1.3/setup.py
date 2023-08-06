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
    'version': '0.1.3',
    'description': 'A python package to automatically generate API documents for Python modules.',
    'long_description': '# Sophia-doc\n\n**A python package to automatically generate API documents for Python modules.**\n\n## Introduction\n\nSophia is a python package to automatically generate API documents for Python modules.\n\nIt\'s a lot like sphinx, but it only focuses on generating markdown documentation.\n\nIt does not support PEP 224 attribute docstrings, because the PEP was rejected, and have to use ast module to support\nit, which brings additional complexity to this project.\n\n# Install\n\n```shell\npip install sophia-doc\n```\n\n# Quickstart\n\n```shell\nsophia_doc "sophia_doc" -o ./doc\n```\n\n## Usage\n\nCommand line:\n\n```shell\nusage: sophia_doc [-h] [-o OUTPUT_DIR] [--docstring-style DOCSTRING_STYLE] [--anchor-extend | --no-anchor-extend] [--overwrite | --no-overwrite]\n                   [--exclude-module-name | --no-exclude-module-name]\n                   module\n\nSophia_doc is a python package to automatically generate API documents for Python modules\n\npositional arguments:\n  module                Python module names.\n\noptions:\n  -h, --help            show this help message and exit\n  -o OUTPUT_DIR, --output-dir OUTPUT_DIR\n                        The directory to write document. (default: doc)\n  --docstring-style DOCSTRING_STYLE\n                        Docstring style the python module used. (default: auto)\n  --anchor-extend, --no-anchor-extend\n                        Add anchor to markdown title. (default: False)\n  --overwrite, --no-overwrite\n                        Overwrite any file in output directory. (default: False)\n  --exclude-module-name, --no-exclude-module-name\n                        Write file to path which exclude module name. (default: False)\n```\n\n## License\n\nMIT © st1020',
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
