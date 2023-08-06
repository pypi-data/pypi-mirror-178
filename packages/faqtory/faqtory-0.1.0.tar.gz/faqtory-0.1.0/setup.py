# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['faqtory']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'jinja2>=3.1.2,<4.0.0', 'rich>=12.6.0,<13.0.0']

entry_points = \
{'console_scripts': ['faq = faqtory.cli:run']}

setup_kwargs = {
    'name': 'faqtory',
    'version': '0.1.0',
    'description': 'Auto FAQ builder',
    'long_description': '',
    'author': 'Will McGugan',
    'author_email': 'willmcgugan@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
