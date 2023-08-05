# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bag',
 'bag.git',
 'bag.spreadsheet',
 'bag.sqlalchemy',
 'bag.text',
 'bag.web',
 'bag.web.pyramid',
 'bag.web.pyramid.apps']

package_data = \
{'': ['*'],
 'bag': ['locale/*', 'locale/pt_BR/LC_MESSAGES/*'],
 'bag.web': ['jinja2/*']}

install_requires = \
['argh', 'polib']

entry_points = \
{'babel.extractors': ['jquery_templates = '
                      'bag.web.transecma:extract_jquery_templates'],
 'console_scripts': ['check_rst = bag.check_rst:command',
                     'delete_old_branches = '
                     'bag.git.delete_old_branches:_command',
                     'po2json = bag.web.transecma:po2json_command',
                     'reorder_po = bag.reorder_po:_command',
                     'replace_many = bag.replace_many:_command']}

setup_kwargs = {
    'name': 'bag',
    'version': '5.0.1',
    'description': 'A library for several purposes',
    'long_description': 'None',
    'author': 'Nando Florestan',
    'author_email': 'nandoflorestan@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/nandoflorestan/bag',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
