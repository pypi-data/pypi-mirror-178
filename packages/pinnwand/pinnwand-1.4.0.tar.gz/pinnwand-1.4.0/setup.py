# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pinnwand', 'pinnwand.handler']

package_data = \
{'': ['*'], 'pinnwand': ['page/*', 'static/*', 'template/*', 'template/part/*']}

install_requires = \
['click>=8.1,<9.0',
 'docutils>=0.19,<0.20',
 'pygments-better-html>=0.1.4,<0.2.0',
 'pygments>=2.13,<3.0',
 'sqlalchemy>=1.4,<2.0',
 'token-bucket>=0.3.0,<0.4.0',
 'tornado>=6.2,<7.0']

extras_require = \
{':python_version < "3.11"': ['tomli>=2.0.1,<3.0.0']}

entry_points = \
{'console_scripts': ['pinnwand = pinnwand.__main__:main']}

setup_kwargs = {
    'name': 'pinnwand',
    'version': '1.4.0',
    'description': 'Straightforward pastebin software.',
    'long_description': '![pinnwand logo, a rabbit](https://pinnwand.readthedocs.io/en/latest/_static/logo-doc.png)\n\n# pinnwand\n\n[![](https://travis-ci.org/supakeen/pinnwand.svg?branch=master)](https://travis-ci.org/supakeen/pinnwand) [![](https://readthedocs.org/projects/pinnwand/badge/?version=latest)](https://pinnwand.readthedocs.io/en/latest/) [![](https://pinnwand.readthedocs.io/en/latest/_static/license.svg)](https://github.com/supakeen/pinnwand/blob/master/LICENSE) [![](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black) [![](https://img.shields.io/pypi/v/pinnwand)](https://pypi.org/project/pinnwand) [![](https://codecov.io/gh/supakeen/pinnwand/branch/master/graph/badge.svg)](https://codecov.io/gh/supakeen/pinnwand) [![](https://quay.io/repository/supakeen/pinnwand/status)](https://quay.io/repository/supakeen/pinnwand)\n\n## About\n\n`pinnwand` is Python pastebin software that tried to keep it simple but got\na little more complex.\n\nPrerequisites\n=============\n* Python >= 3.7\n* Tornado\n* sqlalchemy\n* click\n* docutils\n* tomli\n* pygments-better-html\n* a database driver\n\nUsage\n=====\n\nWeb\n---\nEnter text, click "Paste", easy enough.\n\nsteck\n-----\n[steck](https://supakeen.com/project/steck) is a command line client to pinnwand instances:\n\n```\n€ pip install --user steck\n...\n€ steck paste *\nYou are about to paste the following 7 files. Do you want to continue?\n- LICENSE\n- mypy.ini\n- poetry.lock\n- pyproject.toml\n- README.rst\n- requirements.txt\n- steck.py\n\nContinue? [y/N] y\n\nCompleted paste.\nView link:    https://localhost:8000/W5\nRemoval link: https://localhost:8000/remove/TS2AFFIEHEWUBUV5HLKNAUZFEI\n```\n\ncurl\n----\n`pinnwand` has a direct endpoint for `curl` users:\n\n```\n€ echo "foo" | curl -X POST http://localhost:8000/curl -F \'raw=<-\'\nPaste URL:   http://localhost:8000/OE\nRaw URL:     http://localhost:8000/raw/GU\nRemoval URL: http://localhost:8000/remove/GQBHGJYKRWIS34D6FNU6CJ3B5M\n€ curl http://localhost:8000/raw/GU\nfoo%\n```\n\nThis will preselect the `lexer` and `expiry` arguments to be `text` and\n`1day` respectively. You can provide those to change them.\n\nAPI\n---\n`pinnwand` provides a straight forward JSON API, here\'s an example using the\ncommon requests library:\n\n```\n>>> requests.post(\n...     "http://localhost:8000/api/v1/paste",\n...     json={\n...             "expiry": "1day",\n...             "files": [\n...                     {"name": "spam", "lexer": "python", "content": "eggs"},\n...             ],\n...     }\n... ).json()\n{\'link\': \'http://localhost:8000/74\', \'removal\': \'http://localhost:8000/remove/KYXQLPZQEWV2L4YZM7NYGTR7TY\'}\n```\n\nMore information about this API is available in the [documentation](https://pinnwand.readthedocs.io/en/latest/).\n\n\nMore ways to use pinnwand\n-------------------------\nVarious deprecated ways of posting are still supported, don\'t implement these\nfor any new software but if you are maintaining old software and want to know\nhow they used to work you can read our documentation_.\n\nIf you do use a deprecated endpoint to post a warning will be shown below any\npastes that are created this way.\n\nReporting bugs\n==============\nBugs are reported best at `pinnwand`\'s [project page](https://github.com/supakeen/pinnwand) on github. If you just\nwant to hang out and chat about `pinnwand` then I\'m available in the\n`#pinnwand` channel on Freenode IRC.\n\nLicense\n=======\n`pinnwand` is distributed under the MIT license. See `LICENSE`\nfor details.\n\nHistory\n=======\nThis pastebin has quite a long history which isn\'t reflected entirely in its\nrepository.\n',
    'author': 'Simon de Vlieger',
    'author_email': 'cmdr@supakeen.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/supakeen/pinnwand',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
