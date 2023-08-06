# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oda_data',
 'oda_data..raw_data',
 'oda_data.classes',
 'oda_data.clean_data',
 'oda_data.get_data',
 'oda_data.indicators',
 'oda_data.read_data']

package_data = \
{'': ['*']}

install_requires = \
['bblocks>=0.4.1,<0.5.0',
 'beautifulsoup4>=4.11.1,<5.0.0',
 'pandas>=1.5.2,<2.0.0',
 'pydeflate>=1.2.4,<2.0.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'oda-data',
    'version': '0.1.7',
    'description': 'A python package to work with Official Development Assistance data from the OECD DAC.',
    'long_description': '# oda_data_package\nA python package to access DAC ODA data\n',
    'author': 'Jorge Rivera',
    'author_email': 'jorge.rivera@one.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
