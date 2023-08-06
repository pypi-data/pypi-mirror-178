# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['runner']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cch-runner',
    'version': '0.1.0',
    'description': 'Provide interface for cch Runners.',
    'long_description': '==========\ncch Runner\n==========\n----------------------------------\nProvide interface for cch Runners.\n----------------------------------\n\nHow to use\n----------\n\nDownload using `pip install cch-runner`.\nAdd as a Poetry dependancy using `poetry add cch-runner`.\n\nThis project is not in a stable release, stay updated!\n',
    'author': 'Daniele Tentoni',
    'author_email': 'daniele.tentoni.1996@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
