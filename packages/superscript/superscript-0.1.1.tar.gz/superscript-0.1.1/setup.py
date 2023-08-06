# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['superscript']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.7,<4.0.0',
 'pyyaml>=5.3.1,<6.0.0',
 'requests>=2.24.0,<3.0.0',
 'rich>=4.2.2,<5.0.0',
 'typer[all]>=0.3.1,<0.4.0']

entry_points = \
{'console_scripts': ['superscript = superscript.main:app']}

setup_kwargs = {
    'name': 'superscript',
    'version': '0.1.1',
    'description': 'Dynamical software components manager.',
    'long_description': '# superscript\n\nAwesome superscript to dynamically manage your software components.\n',
    'author': 'toxicphreAK',
    'author_email': 'pentesting.laboratories@gmail.com',
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
