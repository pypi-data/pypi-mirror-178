# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['verylittlewire']

package_data = \
{'': ['*']}

install_requires = \
['pyusb>=1.2.1,<2.0.0']

extras_require = \
{'docs': ['Sphinx>=5.0,<6.0',
          'sphinx-rtd-theme>=1.0,<2.0',
          'myst-parser>=0.18,<0.19']}

setup_kwargs = {
    'name': 'verylittlewire',
    'version': '0.3.0',
    'description': 'The Little Wire Python library provides an interface to the Little Wire USB Multi-Tool developed by Ihsan Kehribar.',
    'long_description': '# Little Wire Python library\n\n<p align="center">\n  <a href="https://github.com/tiacsys/verylittlewire/actions?query=workflow%3ACI">\n    <img src="https://img.shields.io/github/workflow/status/tiacsys/verylittlewire/CI/main?label=CI&logo=github&style=flat-square" alt="CI Status" >\n  </a>\n  <a href="https://verylittlewire.readthedocs.io">\n    <img src="https://img.shields.io/readthedocs/verylittlewire.svg?logo=read-the-docs&logoColor=fff&style=flat-square" alt="Documentation Status">\n  </a>\n  <a href="https://codecov.io/gh/tiacsys/verylittlewire">\n    <img src="https://img.shields.io/codecov/c/github/tiacsys/verylittlewire.svg?logo=codecov&logoColor=fff&style=flat-square" alt="Test coverage percentage">\n  </a>\n</p>\n<p align="center">\n  <a href="https://python-poetry.org/">\n    <img src="https://img.shields.io/badge/packaging-poetry-299bd7?style=flat-square&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAASCAYAAABrXO8xAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAJJSURBVHgBfZLPa1NBEMe/s7tNXoxW1KJQKaUHkXhQvHgW6UHQQ09CBS/6V3hKc/AP8CqCrUcpmop3Cx48eDB4yEECjVQrlZb80CRN8t6OM/teagVxYZi38+Yz853dJbzoMV3MM8cJUcLMSUKIE8AzQ2PieZzFxEJOHMOgMQQ+dUgSAckNXhapU/NMhDSWLs1B24A8sO1xrN4NECkcAC9ASkiIJc6k5TRiUDPhnyMMdhKc+Zx19l6SgyeW76BEONY9exVQMzKExGKwwPsCzza7KGSSWRWEQhyEaDXp6ZHEr416ygbiKYOd7TEWvvcQIeusHYMJGhTwF9y7sGnSwaWyFAiyoxzqW0PM/RjghPxF2pWReAowTEXnDh0xgcLs8l2YQmOrj3N7ByiqEoH0cARs4u78WgAVkoEDIDoOi3AkcLOHU60RIg5wC4ZuTC7FaHKQm8Hq1fQuSOBvX/sodmNJSB5geaF5CPIkUeecdMxieoRO5jz9bheL6/tXjrwCyX/UYBUcjCaWHljx1xiX6z9xEjkYAzbGVnB8pvLmyXm9ep+W8CmsSHQQY77Zx1zboxAV0w7ybMhQmfqdmmw3nEp1I0Z+FGO6M8LZdoyZnuzzBdjISicKRnpxzI9fPb+0oYXsNdyi+d3h9bm9MWYHFtPeIZfLwzmFDKy1ai3p+PDls1Llz4yyFpferxjnyjJDSEy9CaCx5m2cJPerq6Xm34eTrZt3PqxYO1XOwDYZrFlH1fWnpU38Y9HRze3lj0vOujZcXKuuXm3jP+s3KbZVra7y2EAAAAAASUVORK5CYII=" alt="Poetry">\n  </a>\n  <a href="https://github.com/ambv/black">\n    <img src="https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square" alt="black">\n  </a>\n  <a href="https://github.com/pre-commit/pre-commit">\n    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat-square" alt="pre-commit">\n  </a>\n</p>\n<p align="center">\n  <a href="https://pypi.org/project/verylittlewire/">\n    <img src="https://img.shields.io/pypi/v/verylittlewire.svg?logo=python&logoColor=fff&style=flat-square" alt="PyPI Version">\n  </a>\n  <img src="https://img.shields.io/pypi/pyversions/verylittlewire.svg?style=flat-square&logo=python&amp;logoColor=fff" alt="Supported Python versions">\n  <img src="https://img.shields.io/pypi/l/verylittlewire.svg?style=flat-square" alt="License">\n</p>\n\nThe Little Wire Python library provides an interface to the Little Wire USB Multi-Tool developed by Ihsan Kehribar.\n\n## Installation\n\nInstall this via pip (or your favourite package manager):\n\n`pip install verylittlewire`\n\n## Contributors ✨\n\nThanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):\n\n<!-- prettier-ignore-start -->\n<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->\n<!-- prettier-ignore-start -->\n<!-- markdownlint-disable -->\n<table>\n  <tbody>\n    <tr>\n      <td align="center" valign="top" width="14.28%"><a href="http://www.li-pro.net/stephan-linz.phtml"><img src="https://avatars.githubusercontent.com/u/5664060?v=4?s=80" width="80px;" alt="Stephan Linz"/><br /><sub><b>Stephan Linz</b></sub></a><br /><a href="https://github.com/tiacsys/verylittlewire/commits?author=rexut" title="Code">💻</a> <a href="#ideas-rexut" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/tiacsys/verylittlewire/commits?author=rexut" title="Documentation">📖</a></td>\n      <td align="center" valign="top" width="14.28%"><a href="https://github.com/adajoh99"><img src="https://avatars.githubusercontent.com/u/1729678?v=4?s=80" width="80px;" alt="Adam Johnson"/><br /><sub><b>Adam Johnson</b></sub></a><br /><a href="https://github.com/tiacsys/verylittlewire/commits?author=adajoh99" title="Code">💻</a></td>\n      <td align="center" valign="top" width="14.28%"><a href="https://soundcloud.com/ihsankehribar/sets/bits-and-pieces"><img src="https://avatars.githubusercontent.com/u/360652?v=4?s=80" width="80px;" alt="Ihsan Kehribar"/><br /><sub><b>Ihsan Kehribar</b></sub></a><br /><a href="#ideas-kehribar" title="Ideas, Planning, & Feedback">🤔</a></td>\n      <td align="center" valign="top" width="14.28%"><a href="http://omer.kilic.name/"><img src="https://avatars.githubusercontent.com/u/9847?v=4?s=80" width="80px;" alt="Omer Kilic"/><br /><sub><b>Omer Kilic</b></sub></a><br /><a href="#ideas-omerk" title="Ideas, Planning, & Feedback">🤔</a></td>\n    </tr>\n  </tbody>\n</table>\n\n<!-- markdownlint-restore -->\n<!-- prettier-ignore-end -->\n\n<!-- ALL-CONTRIBUTORS-LIST:END -->\n<!-- prettier-ignore-end -->\n\nThis project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!\n\n## Credits\n\nThis package was created with\n[Cookiecutter](https://github.com/audreyr/cookiecutter) and the\n[browniebroke/cookiecutter-pypackage](https://github.com/browniebroke/cookiecutter-pypackage)\nproject template.\n',
    'author': 'Stephan Linz',
    'author_email': 'linz@li-pro.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tiacsys/verylittlewire',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
