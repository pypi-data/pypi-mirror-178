# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['abilian_devtools']

package_data = \
{'': ['*']}

install_requires = \
['black',
 'deptry',
 'docformatter',
 'flake8-bandit',
 'flake8-bugbear',
 'flake8-cognitive-complexity',
 'flake8-comprehensions',
 'flake8-datetimez',
 'flake8-functions',
 'flake8-mutable',
 'flake8-pytest',
 'flake8-simplify',
 'flake8-super',
 'flake8-super-call',
 'flake8-tidy-imports',
 'flake8-tuple',
 'flake8>=6,<7',
 'isort',
 'mypy',
 'nox',
 'pep8-naming',
 'pyright',
 'pytest-cov>=4,<5',
 'pytest-xdist',
 'pytest>=7,<8',
 'reuse',
 'ruff',
 'vulture']

setup_kwargs = {
    'name': 'abilian-devtools',
    'version': '0.1.0',
    'description': 'A curated set of dependencies for quality software development',
    'long_description': 'Nothing here (yet).',
    'author': 'Stefane Fermigier',
    'author_email': 'sf@abilian.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
