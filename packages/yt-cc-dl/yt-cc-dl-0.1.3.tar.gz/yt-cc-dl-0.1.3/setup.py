# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yt_cc_dl']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0', 'requests>=2.2', 'tqdm>=4.0', 'yt-dlp==2022.11.11']

entry_points = \
{'console_scripts': ['yt-cc-dl = yt_cc_dl.cli:main']}

setup_kwargs = {
    'name': 'yt-cc-dl',
    'version': '0.1.3',
    'description': 'Command-line program to download closed captions (subtitles) of videos from YouTube.com',
    'long_description': '# Yt-cc-dl\n\n🚀 Command-line program to download cleaned up closed captions (subtitles) of channels from YouTube.com in JSON format.\n\n[![Supported Python versions](https://img.shields.io/badge/Python-%3E=3.7-blue.svg)](https://www.python.org/downloads/) [![PEP8](https://img.shields.io/badge/Code%20style-PEP%208-orange.svg)](https://www.python.org/dev/peps/pep-0008/) \n\n\n## Requirements\n- 🐍 [python>=3.7](https://www.python.org/downloads/)\n\n\n## ⬇️ Installation\n\n```sh\npip install -U yt-cc-dl\n```\n\n\n## ⌨️ Usage\n\n```\n➜ yt-cc-dl --help\n\nusage: yt-cc-dl [-h] [-o OUTPUT_DIR] [-l LANGUAGES] [-i INDENT] [-r] [-d]\n              channel [channel ...]\n\npositional arguments:\n  channel               Single or multiple YouTube channel URL(s)\n\noptions:\n  -h, --help            show this help message and exit\n  -o OUTPUT_DIR, --output-dir OUTPUT_DIR\n                        Output directory name or path (default: channel name)\n  -l LANGUAGES, --languages LANGUAGES\n                        Comma-separated list of languages to download (can be\n                        regex). The list may contain "all" for all available\n                        languages. The language can be prefixed with a "-" to\n                        exclude it from the requested languages (e.g.,\n                        all,-live_chat)\n  -i INDENT, --indent INDENT\n                        Indentation size in the output JSON files (None by\n                        default)\n  -r, --rich-data       Add a unique index and include the title and thumbnail\n                        in every subtitle entry (useful for Meilisearch)\n  -d, --disable-multithreading\n                        Disable multithreading\n```\n\n## 📝 Todo\n\n- [ ] Enable downloading the cc of a single video.\n',
    'author': 'Alyetama',
    'author_email': 'malyetama@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
