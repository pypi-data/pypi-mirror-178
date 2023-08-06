# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tap_sec', 'tap_sec.core_scraper', 'tap_sec.tests']

package_data = \
{'': ['*']}

install_requires = \
['atomicwrites>=1.4.1,<2.0.0',
 'beautifulsoup4>=4.11.1,<5.0.0',
 'lxml>=4.9.1,<5.0.0',
 'pandas>=1.5.2,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'singer-sdk>=0.14.0,<0.15.0']

extras_require = \
{'s3': ['fs-s3fs>=1.1.1,<2.0.0']}

entry_points = \
{'console_scripts': ['tap-sec = tap_sec.tap:TapSEC.cli']}

setup_kwargs = {
    'name': 'tap-sec',
    'version': '0.0.1',
    'description': '`tap-sec` is a Singer tap for tap-sec, built with the Meltano Singer SDK.',
    'long_description': None,
    'author': 'emcp',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
