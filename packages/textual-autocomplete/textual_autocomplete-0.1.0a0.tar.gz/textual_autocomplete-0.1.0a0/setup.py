# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['textual_autocomplete']

package_data = \
{'': ['*']}

install_requires = \
['textual>=0.5.0']

setup_kwargs = {
    'name': 'textual-autocomplete',
    'version': '0.1.0a0',
    'description': 'Easily add autocomplete dropdowns to your Textual apps.',
    'long_description': '',
    'author': 'Darren Burns',
    'author_email': 'darrenb900@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.8,<4.0.0',
}


setup(**setup_kwargs)
