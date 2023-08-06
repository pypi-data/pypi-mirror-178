# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['faqtory']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'jinja2>=3.1.2,<4.0.0',
 'python-frontmatter>=1.0.0,<2.0.0',
 'pyyaml>=6.0,<7.0',
 'rich>=12.6.0,<13.0.0']

entry_points = \
{'console_scripts': ['faqtory = faqtory.cli:run']}

setup_kwargs = {
    'name': 'faqtory',
    'version': '0.2.0',
    'description': 'Auto FAQ builder',
    'long_description': '# FAQtory\n\nThis is a tool to auto-generate Frequently Asked Questions (FAQs) documents.\n\nFAQtory compiles a [FAQ.md](./FAQ.md) from individual `.question.md` documents. By default this will create a GitHub flavoured Markdown document, but you can edit a template to produce whatever format you like.\n\n## Getting started\n\nInstall `faqtory` from PyPI. I\'m going to assume you know how to do this bit.\n\nRun the following from the directory you wish to store the FAQ document. \n\n```bash\nfaqtory init\n```\n\nThis will create the following files and directories:\n\n- `faq.yml` A configuration file which you can edit.\n- `./.faq/` A directory which stores templates.\n- `./questions/` A directory containing question documents.\n\n## Adding questions\n\nTo add questions create a file with the extension `.question.md` in the questions directory (`./questions/` if you are using the defaults).\n\nQuestion documents are Markdown with front-matter. Here\'s an example:\n\n```yml\n---\ntitle: "What does FAQ stand for?"\n\n---\n\nFAQ stands for *Frequently Asked Questions*\n```\n\nThe filename is unimportant, but a `title` is mandatory. The body of the question can include any Markdown.\n\n## Building\n\nRun the following command to build the FAQ:\n\n```bash\nfaqtory build\n```\n\nWith the default settings this will generate an [FAQ.md](./FAQ.md) file.\n\n## Roadmap\n\nFAQtory is a work in progress, and a few hours work. The ultimate goal is to build a GitHub action that suggests answers to an issue from the FAQ.\n',
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
