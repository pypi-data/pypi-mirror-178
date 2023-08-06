# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['textualitty']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'rich>=12.6.0,<13.0.0', 'tomlkit>=0.11.6,<0.12.0']

entry_points = \
{'console_scripts': ['textualitty = textualitty.app:run']}

setup_kwargs = {
    'name': 'textualitty',
    'version': '0.2.7',
    'description': '',
    'long_description': '# Textualitty\n\nTextualitty bundles your [textual](https://textual.textualize.io) apps into standalone executables.\n\nCurrenly supports MacOS only. Windows and Linux to follow.\n',
    'author': 'Felix Ingram',
    'author_email': 'f.ingram@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
