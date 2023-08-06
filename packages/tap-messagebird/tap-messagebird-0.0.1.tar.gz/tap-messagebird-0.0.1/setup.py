# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tap_messagebird', 'tap_messagebird.tests']

package_data = \
{'': ['*'], 'tap_messagebird': ['schemas/*']}

install_requires = \
['requests>=2.25.1,<3.0.0', 'singer-sdk>=0.14.0,<0.15.0']

extras_require = \
{'s3': ['fs-s3fs>=1.1.1,<2.0.0']}

entry_points = \
{'console_scripts': ['tap-messagebird = '
                     'tap_messagebird.tap:TapMessagebird.cli']}

setup_kwargs = {
    'name': 'tap-messagebird',
    'version': '0.0.1',
    'description': '`tap-messagebird` is a Singer tap for Messagebird, built with the Meltano Singer SDK.',
    'long_description': None,
    'author': 'Meltano',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
