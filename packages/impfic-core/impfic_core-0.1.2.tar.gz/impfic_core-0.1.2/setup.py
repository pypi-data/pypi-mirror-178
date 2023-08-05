# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['impfic_core', 'impfic_core.parse', 'impfic_core.resources']

package_data = \
{'': ['*']}

install_requires = \
['numpy', 'pandas']

entry_points = \
{'console_scripts': ['version = poetry_scripts:version']}

setup_kwargs = {
    'name': 'impfic-core',
    'version': '0.1.2',
    'description': 'Utility functions for the Impact and Fiction project',
    'long_description': "# impfic-core\n\n[![GitHub Actions](https://github.com/impact-and-fiction/impfic-core/workflows/tests/badge.svg)](https://github.com/impact-and-fiction/impfic-core/actions)\n[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)\n[![PyPI](https://img.shields.io/pypi/v/impfic-core)](https://pypi.org/project/impfic-core/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/impfic-core)](https://pypi.org/project/impfic-core/)\n\nCore code base for common functionalities\n\n## Installing\n\n```shell\npip install impfic-core\n```\n\n## Usage\n\nTo use utilities for external resources such as the RBN, you need to point to your copy of those resources \nin the settings (`settings.py`). Once you have done that, you can use them with:\n\n```python\nfrom settings import rbn_file\nfrom impfic_core.resources.rbn import RBN\n\nrbn = RBN(rbn_file)\n\nrbn.has_term('aanbiddelijk') # returns True\n```\n",
    'author': 'Marijn Koolen',
    'author_email': 'marijn.koolen@huygens.knaw.nl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/impact-and-fiction/impfic-core',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
