# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['owl_finder']

package_data = \
{'': ['*']}

install_requires = \
['baseblock']

setup_kwargs = {
    'name': 'owl-finder',
    'version': '0.1.0',
    'description': 'Perform Ontology Queries with a Finder Facade',
    'long_description': '# Ontology Finder (owl-finder)\nA Finder Facade for Querying Ontology Files\n',
    'author': 'Craig Trim',
    'author_email': 'craigtrim@gmail.com',
    'maintainer': 'Craig Trim',
    'maintainer_email': 'craigtrim@gmail.com',
    'url': 'https://github.com/craigtrim/owl-finder',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.5,<4.0.0',
}


setup(**setup_kwargs)
