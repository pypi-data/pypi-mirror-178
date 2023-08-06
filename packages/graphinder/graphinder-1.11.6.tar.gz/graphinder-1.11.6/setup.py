# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['graphinder',
 'graphinder.entities',
 'graphinder.io',
 'graphinder.pool',
 'graphinder.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp[speedups]>=3.8.1,<4.0.0',
 'beautifulsoup4>=4,<5',
 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['graphinder = graphinder:cli']}

setup_kwargs = {
    'name': 'graphinder',
    'version': '1.11.6',
    'description': 'Escape Graphinder',
    'long_description': '# Graphinder ![PyPI](https://img.shields.io/pypi/v/graphinder) [![CI](https://github.com/Escape-Technologies/graphinder/actions/workflows/ci.yaml/badge.svg)](https://github.com/Escape-Technologies/graphinder/actions/workflows/ci.yaml) [![codecov](https://codecov.io/gh/Escape-Technologies/graphinder/branch/main/graph/badge.svg?token=4KGK1LTHRO)](https://codecov.io/gh/Escape-Technologies/graphinder)\n\nGraphinder is a tool that extracts all GraphQL endpoints from a given domain.\n\n![Banner](doc/banner.png)\n\n![Docker Pulls](https://img.shields.io/docker/pulls/escapetech/graphinder)\n![Docker Image Size (latest by date)](https://img.shields.io/docker/image-size/escapetech/graphinder)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/graphinder)\n\n## Run with docker\n\n```bash\ndocker pull escapetech/graphinder\ndocker run -it --rm escapetech/graphinder -d example.com\n```\n\nIf you want to save your results.json file, you can use:\n\n```bash\ndocker run -it --name graphinder escapetech/graphinder -d example.com\ndocker cp graphinder:/graphinder/results.json results.json\ndocker rm -f graphinder\n```\n\nOr if you want to pass a file containing domain names (one per line):\n\n```bash\ndocker run -v /full/path/to/file.csv:/graphinder/file.csv -it --rm escapetech/graphinder --inplace -f /graphinder/file.csv\n```\n\n## Install using Pip\n\n```bash\npip install graphinder\n\n# using specific python binary\npython3 -m pip install graphinder\n```\n\nRun it with\n\n```bash\ngraphinder ...\n```\n\n## Usage\n\nA Scan consistes of:\n\n- Running on a specific domain (`-d`, `--domain`) or a list of domains (`-f`, `--input-file`).\n- Searching all scripts loaded by the browser for graphql endpoint (`-s`, `--script`)\n- Brute forcing the directories of all discovered urls (`-b`, `--bruteforce`)\n- Using precision mode (`-p`, `--precision`)\n\nBy default, bruteforce and script search are enabled.\n\n```bash\ngraphinder -d example.com\n```\n\n```bash\ngraphinder -f domains.txt\n```\n\n### Extra features\n\n- `--no-bruteforce`: Disable bruteforce\n- `--no-script`: Disable script search\n- `-p --precision --no-precision`: Enable/disable precision mode (default: enabled) (precision mode is slower but more accurate)\n- `-f --input-file <FILE_PATH>`: Input domain names from file\n- `-w --max-workers <int>`: Maximum of concurrent workers on multiple domains.\n- `-o --output-file <FILE_PATH>`: Output the results to file\n- `-v --verbose --no-verbose`: Verbose mode\n- `-r --reduce`: The maximum number of subdomains to scan.\n- `-wb --webhook_url`: The discord webhook url to send the results to.\n\nIf you experience any issues, irregularities or networking bottlenecks, please reduce your number of workers, otherwise, better is your network, the more workers you can have.\n\n## Local installation\n\nClone the repository and run the installation script\n\n```bash\ngit clone https://github.com/Escape-Technologies/graphinder.git\ncd Graphinder\n./install-dev.sh\n```\n\nRun this command to enter the virtual enviroment\n\n```bash\npoetry shell\n```\n\nProfit !\n\n```bash\ngraphinder -d example.com\n```\n\n## How do you make sure this is a valid graphql endpoint ?\n\n![detector](doc/detector.jpg)\n\n## Contributing\n\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n## License ![PyPI - License](https://img.shields.io/pypi/l/graphinder)\n\n[MIT](https://choosealicense.com/licenses/mit/)\n',
    'author': 'Escape Technologies SAS',
    'author_email': 'ping@escape.tech',
    'maintainer': 'Karim Rustom',
    'maintainer_email': 'rustom@escape.tech',
    'url': 'https://escape.tech/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
