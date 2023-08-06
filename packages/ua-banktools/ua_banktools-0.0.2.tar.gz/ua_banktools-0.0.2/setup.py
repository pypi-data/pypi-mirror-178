# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ua_banktools', 'ua_banktools.banks', 'ua_banktools.core']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.2,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'schwifty>=2022.9.0,<2023.0.0']

setup_kwargs = {
    'name': 'ua-banktools',
    'version': '0.0.2',
    'description': '',
    'long_description': '# ua_banktools\nA collection of Python tools and APIs for interacting with Ukrainian banks\n',
    'author': 'Anton Shpigunov',
    'author_email': 'shpigunov@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10',
}


setup(**setup_kwargs)
