# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['marini_spreading']

package_data = \
{'': ['*']}

install_requires = \
['pyroll-basic>=1.0.1,<2.0.0']

setup_kwargs = {
    'name': 'pyroll-marini-spreading',
    'version': '1.0.1',
    'description': 'Plugin for PyRoll providing the Marini spreading model.',
    'long_description': 'None',
    'author': 'Christoph Renzing',
    'author_email': 'christoph.renzing@imf.tu-freiberg.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pyroll-project.github.io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
