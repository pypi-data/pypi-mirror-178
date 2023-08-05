# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['plur']
install_requires = \
['flake8-pyproject>=1.2.0,<2.0.0']

setup_kwargs = {
    'name': 'plur',
    'version': '0.2.0',
    'description': 'Simple language universal pluralizer',
    'long_description': '',
    'author': 'Tom Ritchford',
    'author_email': 'tom@swirly.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
