# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['processing',
 'processing.batch',
 'processing.core',
 'processing.export',
 'processing.files',
 'processing.libs',
 'processing.plots']

package_data = \
{'': ['*']}

install_requires = \
['configparser>=5.3.0,<6.0.0',
 'matplotlib>=3.6.2,<4.0.0',
 'numpy>=1.23.5,<2.0.0',
 'scipy>=1.9.3,<2.0.0',
 'tifffile>=2022.10.10,<2023.0.0']

setup_kwargs = {
    'name': 'endopy-ppp',
    'version': '0.1.1',
    'description': 'Public source files for Endopy data post processing. Written in Python 3.',
    'long_description': '# Endopy public post-processing\n\n\nPublic source files for Endopy data post processing.\nIt is written with Python 3.\n\n\n\n## Installation\n\n\n\n\n## Usage\n\n',
    'author': 'jysru',
    'author_email': 'jysru@pm.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
