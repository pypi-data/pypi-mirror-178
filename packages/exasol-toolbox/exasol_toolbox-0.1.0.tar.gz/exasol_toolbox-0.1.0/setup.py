# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['exasol',
 'exasol.toolbox',
 'exasol.toolbox.nox',
 'exasol.toolbox.pre_commit_hooks',
 'exasol.toolbox.sphinx',
 'exasol.toolbox.sphinx.multiversion']

package_data = \
{'': ['*'], 'exasol.toolbox.sphinx.multiversion': ['templates/*']}

install_requires = \
['black>=22.8.0,<23.0.0',
 'coverage>=6.4.4,<7.0.0',
 'furo>=2022.9.15,<2023.0.0',
 'isort>=5.10.1,<6.0.0',
 'mypy>=0.971,<0.972',
 'nox>=2022.8.7,<2023.0.0',
 'pre-commit>=2.20.0,<3.0.0',
 'pylint>=2.15.4,<3.0.0',
 'pytest>=7.1.3,<8.0.0',
 'pyupgrade>=2.38.2,<3.0.0',
 'rich>=12.6.0,<13.0.0',
 'scriv>=0.17.0,<0.18.0',
 'sphinx-copybutton>=0.5.0,<0.6.0',
 'sphinx>=5.3.0,<6.0.0']

entry_points = \
{'console_scripts': ['sphinx-multiversion = '
                     'exasol.toolbox.sphinx.multiversion.main:main',
                     'version-check = '
                     'exasol.toolbox.pre_commit_hooks.package_version:main']}

setup_kwargs = {
    'name': 'exasol-toolbox',
    'version': '0.1.0',
    'description': '',
    'long_description': 'Exasol Toolbox\n#####################\n\n.. image:: https://img.shields.io/pypi/v/exasol-toolbox\n     :target: https://pypi.org/project/exasol-toolbox/\n     :alt: PyPI Version\n\n.. image:: https://img.shields.io/pypi/pyversions/exasol-toolbox\n    :target: https://pypi.org/project/exasol-toolbox\n    :alt: PyPI - Python Version\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n    :alt: Formatter - Black\n\n.. image:: https://img.shields.io/badge/imports-isort-ef8336.svg\n    :target: https://pycqa.github.io/isort/\n    :alt: Formatter - Isort\n\n.. image:: https://img.shields.io/badge/typing-mypy-blue\n    :target: https://github.com/PyCQA/pylint\n    :alt: Pylint\n\n.. image:: https://img.shields.io/badge/pylint-7.8-green\n    :target: https://github.com/PyCQA/pylint\n    :alt: Pylint\n\n.. image:: https://img.shields.io/pypi/l/exasol-bucketfs\n     :target: https://opensource.org/licenses/MIT\n     :alt: License\n\n.. image:: https://img.shields.io/github/last-commit/nicoretti/python-toolbox\n     :target: https://pypi.org/project/exasol-toolbox/\n     :alt: Last Commit\n\n\n🚀 Features\n------------\n\n* Centrally managed standard tasks\n    - code formatting & upgrading\n    - linting\n    - type-checking\n    - unit-tests\n    - integration-tests\n    - coverage\n    - documentation\n\n* Centrally manged core workflows\n    - workspace/project verification\n    - build and publish releases\n    - build and publish documentation\n\n* Configurable & Extensible\n    - Project configuration\n    - Event hooks\n\n🔌️ Prerequisites\n-----------------\n\n- `Python <https://www.python.org/>`_ >= 3.8\n\n💾 Installation\n----------------\n\n.. code-block:: shell\n\n    pip install exasol-toolbox\n\n📚 Documentation\n----------------\n\nThe latest documentation can be found `here <https://nicoretti.github.io/python-toolbox/index.html>`_.\n',
    'author': 'Nicola Coretti',
    'author_email': 'nicola.coretti@exasol.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
