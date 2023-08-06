# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pytest_failed_screen_record']
install_requires = \
['PyAutoGUI>=0.9.53,<0.10.0',
 'numpy>=1.23.5,<2.0.0',
 'opencv-python>=4.6.0,<5.0.0',
 'pytest>=7.1.2d,<8.0.0']

entry_points = \
{'pytest11': ['failed_screen_record = pytest_failed_screen_record']}

setup_kwargs = {
    'name': 'pytest-failed-screen-record',
    'version': '0.1.1',
    'description': 'Create a video of the screen when pytest fails',
    'long_description': '===========================\npytest-failed-screen-record\n===========================\n\n.. image:: https://img.shields.io/pypi/v/pytest-failed-screen-record.svg\n    :target: https://pypi.org/project/pytest-failed-screen-record\n    :alt: PyPI version\n\n.. image:: https://img.shields.io/pypi/pyversions/pytest-failed-screen-record.svg\n    :target: https://pypi.org/project/pytest-failed-screen-record\n    :alt: Python versions\n\n.. image:: https://ci.appveyor.com/api/projects/status/github/KeisukeShima/pytest-failed-screen-record?branch=master\n    :target: https://ci.appveyor.com/project/KeisukeShima/pytest-failed-screen-record/branch/master\n    :alt: See Build Status on AppVeyor\n\nCreate a video of the screen when pytest fails\n\n----\n\nThis `pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_\'s `cookiecutter-pytest-plugin`_ template.\n\n\nFeatures\n--------\n\n* TODO\n\n\nRequirements\n------------\n\n* TODO\n\n\nInstallation\n------------\n\nYou can install "pytest-failed-screen-record" via `pip`_ from `PyPI`_::\n\n    $ pip install pytest-failed-screen-record\n\n\nUsage\n-----\n\n* TODO\n\nContributing\n------------\nContributions are very welcome. Tests can be run with `tox`_, please ensure\nthe coverage at least stays the same before you submit a pull request.\n\nLicense\n-------\n\nDistributed under the terms of the `MIT`_ license, "pytest-failed-screen-record" is free and open source software\n\n\nIssues\n------\n\nIf you encounter any problems, please `file an issue`_ along with a detailed description.\n\n.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter\n.. _`@hackebrot`: https://github.com/hackebrot\n.. _`MIT`: http://opensource.org/licenses/MIT\n.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause\n.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt\n.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0\n.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin\n.. _`file an issue`: https://github.com/KeisukeShima/pytest-failed-screen-record/issues\n.. _`pytest`: https://github.com/pytest-dev/pytest\n.. _`tox`: https://tox.readthedocs.io/en/latest/\n.. _`pip`: https://pypi.org/project/pip/\n.. _`PyPI`: https://pypi.org/project\n',
    'author': 'Keisuke Shima',
    'author_email': '19993104+KeisukeShima@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/KeisukeShima/pytest-failed-screen-record',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
