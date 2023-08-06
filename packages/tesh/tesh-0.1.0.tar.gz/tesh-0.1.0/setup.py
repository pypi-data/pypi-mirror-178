# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tesh', 'tesh.tests']

package_data = \
{'': ['*'],
 'tesh.tests': ['fixtures/*', 'fixtures/empty_folder/*', 'fixtures/folder/*']}

install_requires = \
['click', 'pexpect']

entry_points = \
{'console_scripts': ['tesh = tesh:tesh']}

setup_kwargs = {
    'name': 'tesh',
    'version': '0.1.0',
    'description': 'TEstable SHell sessions in Markdown',
    'long_description': 'None',
    'author': 'Domen Kozar',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
