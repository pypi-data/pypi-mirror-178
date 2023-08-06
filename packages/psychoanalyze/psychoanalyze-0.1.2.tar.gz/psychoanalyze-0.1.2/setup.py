# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['psychoanalyze']

package_data = \
{'': ['*']}

install_requires = \
['bandit>=1.7.4,<2.0.0',
 'black>=22.3.0,<23.0.0',
 'cmdstanpy>=1.0.8,<2.0.0',
 'dash-bootstrap-components>=1.1.0,<2.0.0',
 'dash-daq>=0.5.0,<0.6.0',
 'dash[testing]>=2.7.0,<3.0.0',
 'datatest>=0.11.1,<0.12.0',
 'flake8>=4.0.1,<5.0.0',
 'gunicorn>=20.1.0,<21.0.0',
 'hypothesis>=6.50.0,<7.0.0',
 'importlib-resources>=5.8.0,<6.0.0',
 'kaleido==0.2.1',
 'matplotlib>=3.5.1,<4.0.0',
 'mkdocs-gen-files>=0.3.4,<0.4.0',
 'mkdocs-material>=8.3.9,<9.0.0',
 'mkdocs>=1.3.0,<2.0.0',
 'mkdocstrings>=0.18.1,<0.19.0',
 'mypy>=0.990,<0.991',
 'numpy>=1.23.4,<2.0.0',
 'pandas-stubs>=1.5.1.221024,<2.0.0.0',
 'pandas>=1.4.2,<2.0.0',
 'pandera>=0.11.0,<0.12.0',
 'plotly>=5.11.0,<6.0.0',
 'pre-commit>=2.20.0,<3.0.0',
 'pytest-mock>=3.7.0,<4.0.0',
 'pytest-sugar>=0.9.4,<0.10.0',
 'pytest>=7.2.0,<8.0.0',
 'safety>=2.0.0,<3.0.0',
 'scipy>=1.8.0,<2.0.0',
 'statsmodels>=0.13.2,<0.14.0',
 'tabulate>=0.8.10,<0.9.0']

setup_kwargs = {
    'name': 'psychoanalyze',
    'version': '0.1.2',
    'description': 'A Pythonic analysis package for psychophysics data',
    'long_description': 'None',
    'author': 'Ty Schlichenmeyer',
    'author_email': 'ty.schlich@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.11.0',
}


setup(**setup_kwargs)
