# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pytest_failed_screen_record']
install_requires = \
['PyAutoGUI>=0.9.53,<0.10.0',
 'numpy>=1.23.5,<2.0.0',
 'opencv-python>=4.6.0,<5.0.0',
 'pytest>=7.2.0,<8.0.0']

entry_points = \
{'pytest11': ['failed_screen_record = pytest_failed_screen_record']}

setup_kwargs = {
    'name': 'pytest-failed-screen-record',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Keisuke Shima',
    'author_email': '19993104+KeisukeShima@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
