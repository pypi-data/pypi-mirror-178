# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['heimdall',
 'heimdall.bifrost',
 'heimdall.bifrost.utils',
 'heimdall.cli',
 'heimdall.gjallarhorn',
 'heimdall.gjallarhorn.streamlit',
 'heimdall.gjallarhorn.streamlit.utils',
 'heimdall.gulltoppr',
 'heimdall.gulltoppr.drift_monitor',
 'heimdall.gulltoppr.drift_monitor.algorithms',
 'heimdall.gulltoppr.performance_monitor',
 'heimdall.gulltoppr.performance_monitor.metrics',
 'heimdall.gulltoppr.systems_monitor',
 'heimdall.gulltoppr.systems_monitor.metrics',
 'heimdall.utils']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'aif360>=0.5.0,<0.6.0',
 'click>=8.1.3,<9.0.0',
 'colorlog==6.7.0',
 'google-cloud-bigquery==3.3.2',
 'numpy==1.23.2',
 'pandas-gbq==0.17.8',
 'pandas>=1.4.4,<2.0.0',
 'plotly==5.10.0',
 'redis>=4.3.4,<5.0.0',
 'schedule>=1.1.0,<2.0.0',
 'scikit-learn>=1.1.2,<2.0.0',
 'scipy>=1.9.1,<2.0.0',
 'slack-sdk==3.18.3',
 'streamlit-aggrid>=0.3.3,<0.4.0',
 'streamlit-option-menu>=0.3.2,<0.4.0',
 'streamlit==1.12.2']

entry_points = \
{'console_scripts': ['heimdall = heimdall.cli:cli']}

setup_kwargs = {
    'name': 'heimdall-ml',
    'version': '1.1.15',
    'description': 'Package to monitor machine learning models using .yml files',
    'long_description': 'None',
    'author': 'Ben Hicks',
    'author_email': 'bhicks@uw.co.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.9.7',
}


setup(**setup_kwargs)
