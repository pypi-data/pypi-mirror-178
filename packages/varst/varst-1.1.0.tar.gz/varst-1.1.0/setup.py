# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['varst', 'varst.utils']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['varst = varst.cli:main']}

setup_kwargs = {
    'name': 'varst',
    'version': '1.1.0',
    'description': 'Replace substitutions in rst files with variables.',
    'long_description': '==============================\nvarST(var ➡️ reStructuredText)\n==============================\n\n|PyPI version| |pre-commit.ci status| |GitHub Workflow Status| |Documentation Status|\n\nReplace substitutions in rst files with variables.\n\nInstallation\n------------\n\n.. code:: bash\n\n   $ pip install varst\n\nUsage\n-----\n\n.. code:: bash\n\n   $ varst [-i INPUT] [-o OUTPUT] [name=value ...]\n\nLicense\n-------\n\n`MIT\nLicense <https://github.com/junghoon-vans/varst/blob/main/LICENSE>`__\n\n\n.. |PyPI version| image:: https://img.shields.io/pypi/v/varst\n   :target: https://pypi.org/project/varst/\n.. |pre-commit.ci status| image:: https://results.pre-commit.ci/badge/github/junghoon-vans/varst/main.svg\n   :target: https://results.pre-commit.ci/latest/github/junghoon-vans/varst/main\n.. |GitHub Workflow Status| image:: https://img.shields.io/github/workflow/status/junghoon-vans/varst/Upload%20Python%20Package\n.. |Documentation Status| image:: https://readthedocs.org/projects/varst/badge/?version=latest\n    :target: https://varst.readthedocs.io/en/latest/?badge=latest\n',
    'author': 'Jeonghun-Ban',
    'author_email': 'junghoon.ban@gmail.com',
    'maintainer': 'Jeonghun-Ban',
    'maintainer_email': 'junghoon.ban@gmail.com',
    'url': 'https://github.com/junghoon-vans/varst',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
