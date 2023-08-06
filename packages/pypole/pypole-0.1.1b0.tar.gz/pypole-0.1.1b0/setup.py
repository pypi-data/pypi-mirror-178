# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypole']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.2,<4.0.0',
 'numba>=0.56.4,<0.57.0',
 'numpy>=1.23.4,<2.0.0',
 'pre-commit>=2.20.0,<3.0.0',
 'rich>=10.14.0,<11.0.0',
 'scipy>=1.9.3,<2.0.0',
 'tqdm>=4.64.1,<5.0.0']

entry_points = \
{'console_scripts': ['pypole = pypole.__main__:app']}

setup_kwargs = {
    'name': 'pypole',
    'version': '0.1.1b0',
    'description': 'Awesome `pypole` is a Python cli/package created with https://github.com/TezRomacH/python-package-template',
    'long_description': '# pypole\n\n<div align="center">\n\n[![Build status](https://github.com/pypole/pypole/workflows/build/badge.svg?branch=master&event=push)](https://github.com/pypole/pypole/actions?query=workflow%3Abuild)\n[![Python Version](https://img.shields.io/pypi/pyversions/pypole.svg)](https://pypi.org/project/pypole/)\n[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/pypole/pypole/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)\n[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pypole/pypole/blob/master/.pre-commit-config.yaml)\n[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/pypole/pypole/releases)\n[![License](https://img.shields.io/github/license/pypole/pypole)](https://github.com/pypole/pypole/blob/master/LICENSE)\n![Coverage Report](assets/images/coverage.svg)\n\n`pypole` is a Python package for simple fitting of magnetic dipoles to magnetic maps measured with Quantum diamond microscope or SQUID microscope\n\n</div>\n\n## Installation\n\n```bash\npip install -U pypole\n```\n\nor install with `Poetry`\n\n```bash\npoetry add pypole\n```\n\n## 🛡 License\n\n[![License](https://img.shields.io/github/license/pypole/pypole)](https://github.com/pypole/pypole/blob/master/LICENSE)\n\nThis project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/pypole/pypole/blob/master/LICENSE) for more details.\n\n## 📃 Citation\n\n```bibtex\n@misc{pypole,\n  author = {pypole},\n  title = {Awesome `pypole` is a Python cli/package created with https://github.com/TezRomacH/python-package-template},\n  year = {2022},\n  publisher = {GitHub},\n  journal = {GitHub repository},\n  howpublished = {\\url{https://github.com/pypole/pypole}}\n}\n```\n\n## Credits [![🚀 Your next Python package needs a bleeding-edge project structure.](https://img.shields.io/badge/python--package--template-%F0%9F%9A%80-brightgreen)](https://github.com/TezRomacH/python-package-template)\n\nThis project was generated with [`python-package-template`](https://github.com/TezRomacH/python-package-template)\n',
    'author': 'pypole',
    'author_email': 'michaelvolk1979@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/pypole/pypole',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
