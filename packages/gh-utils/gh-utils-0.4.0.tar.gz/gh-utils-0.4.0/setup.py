# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gh_utils']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0']

entry_points = \
{'console_scripts': ['ghcrar = gh_utils.gh_create_repo_and_add_to_remote:main']}

setup_kwargs = {
    'name': 'gh-utils',
    'version': '0.4.0',
    'description': 'GitHub CLI Utilities',
    'long_description': "# GH Utilities\n\nA collection of useful utilities that work with GitHub CLI `gh`.\n\n- [GH Utilities](#gh-utilities)\n  - [Installation](#installation)\n    - [pipx](#pipx)\n    - [pip](#pip)\n  - [Utilities](#utilities)\n    - [ghcrar](#ghcrar)\n      - [Features](#features)\n      - [Usage](#usage)\n      - [Screenshots](#screenshots)\n\n## Installation\n\n### pipx\n\nThis is the recommended installation method.\n\n```\n$ pipx install gh-utils\n```\n\n### [pip](https://pypi.org/project/gh-utils/)\n\n```\n$ pip install gh-utils\n```\n\n## Utilities\n\n### ghcrar\n\n\n#### Features\n- Custom GitHub instance hostname support with `--hostname`\n- Supports both `ssh` and `https` protocols\n\n#### Usage\n\n```\n$ ghcrar --help\n\nusage: ghcrar [-h] [-a SUFFIX] [-n GITHUB REPO NAME] [--public] [--overwrite-remote-origin] [-H {ssh,https}] [-p PROTOCOL] [-V]\n\nCreate a GitHub repo with gh and add it as a remote\n\noptions:\n  -h, --help            show this help message and exit\n  -a SUFFIX, --append SUFFIX\n                        String to append to the repo name (default: None)\n  -n GITHUB REPO NAME, --name GITHUB REPO NAME\n                        The string to use as GitHub repo name, or <user|org>/<repo-name> with a slash (default: None)\n  --public              Create a public repository (default: False)\n  --overwrite-remote-origin, --force\n                        Overwrites remote origin if exists (default: False)\n  -H {ssh,https}, --hostname {ssh,https}\n                        GitHub hostname, default to use the first entry in hosts.yml (default: github.com)\n  -p PROTOCOL, --protocol PROTOCOL\n                        git protocol (default: ssh)\n  -V, --version         show program's version number and exit\n```\n\n#### Screenshots\n![ghcrar-public](images/ghcrar-public.png)\n\n\n\n",
    'author': 'Xinyuan Chen',
    'author_email': '45612704+tddschn@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tddschn/gh-utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
