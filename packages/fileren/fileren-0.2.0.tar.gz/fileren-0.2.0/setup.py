# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fileren']

package_data = \
{'': ['*']}

install_requires = \
['rich>=12.6.0,<13.0.0']

entry_points = \
{'console_scripts': ['fileren = fileren.main:main']}

setup_kwargs = {
    'name': 'fileren',
    'version': '0.2.0',
    'description': 'Simple tool for renaming files in a directory',
    'long_description': '# Fileren\n\n[PROJECT WEBSITE](https://hawier.dev/projects/other/fileren.html)\n\nSimple tool for renaming files in a directory\n\n![How to use gif](assets/how_to_use.gif)\n\n## Installation\n\n```shell\npip install fileren\n```\n\n## Usage\n\nTo run the program, simply run the following command:\n\n```shell\nfileren\n```\n\nOr run command with arguments:\n\n```shell\nfileren --path {path_to_directory} --regex {regex} --new_string {new_string}\n```\n\nTo insert the current index of the file, use the following syntax as new string:\n\nExample: \n\n```shell\nfileren --path data --regex _text_[0-9]+ --new_string _{i}_\n```\n\nInput:\n\n```shell\ndata\n├── file_text_1.txt\n├── file_text_2.txt\n├── file_text_3.txt\n└── file_text_4.txt\n```\n\nOutput:\n\n```shell\ndata\n├── file_0.txt\n├── file_1.txt\n├── file_2.txt\n└── file_3.txt\n```\n\n',
    'author': 'Mikołaj Badyl',
    'author_email': 'contact@hawier.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
