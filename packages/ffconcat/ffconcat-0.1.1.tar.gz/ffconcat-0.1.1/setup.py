# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ffconcat']

package_data = \
{'': ['*']}

install_requires = \
['ffmpeg>=1.4,<2.0']

entry_points = \
{'console_scripts': ['ffconcat = ffconcat:ffconcat.main']}

setup_kwargs = {
    'name': 'ffconcat',
    'version': '0.1.1',
    'description': 'Easily concat videos with FFmpeg from Python',
    'long_description': '# Ffconcat\n\n🚀 FFmpeg concat videos.\n\n[![Supported Python versions](https://img.shields.io/badge/Python-%3E=3.6-blue.svg)](https://www.python.org/downloads/) [![PEP8](https://img.shields.io/badge/Code%20style-PEP%208-orange.svg)](https://www.python.org/dev/peps/pep-0008/) \n\n\n## Requirements\n- 🐍 [python>=3.6](https://www.python.org/downloads/)\n\n\n## ⬇️ Installation\n\n```sh\npip install ffconcat\n```\n\n\n## ⌨️ Usage\n\n```\n➜ ffconcat --help\n\n\n```\n\n\n## 📕 Examples\n',
    'author': 'Alyetama',
    'author_email': 'malyetama@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
