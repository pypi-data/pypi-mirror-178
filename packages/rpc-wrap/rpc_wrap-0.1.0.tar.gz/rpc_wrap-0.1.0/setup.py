# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rpc_wrap']

package_data = \
{'': ['*']}

install_requires = \
['setuptools>=65.6.0,<66.0.0']

extras_require = \
{'cli': ['click>=8.1.3,<9.0.0',
         'click-log>=0.4.0,<0.5.0',
         'rich>=12.6.0,<13.0.0'],
 'flask': ['flask>=2.2.2,<3.0.0', 'flask-cors>=3.0.10,<4.0.0']}

entry_points = \
{'console_scripts': ['rpc-wrap = rpc_wrap.cli:main'],
 'rpc_wrap': ['sample = rpc_wrap.sample:app']}

setup_kwargs = {
    'name': 'rpc-wrap',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Kaj Siebert',
    'author_email': 'kaj@k-si.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
