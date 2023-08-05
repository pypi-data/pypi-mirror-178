# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dj_link']

package_data = \
{'': ['*']}

modules = \
['link_shortener']
install_requires = \
['pyshorteners>=1.0.1,<2.0.0']

entry_points = \
{'console_scripts': ['djlink = dj_link.Main:cli']}

setup_kwargs = {
    'name': 'dj-link',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'dongjin2008',
    'author_email': '80329234+dongjin2008@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
