# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['calnexus']

package_data = \
{'': ['*']}

install_requires = \
['abydos>=0.5.0,<0.6.0',
 'numpy>=1.23.4,<2.0.0',
 'pandas>=1.5.1,<2.0.0',
 'streamlit>=1.14.1,<2.0.0']

setup_kwargs = {
    'name': 'calnexus',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'krushna Panchvishe',
    'author_email': 'krushnap@cdac.in',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
