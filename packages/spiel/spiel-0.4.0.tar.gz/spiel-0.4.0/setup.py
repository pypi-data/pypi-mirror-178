# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spiel', 'spiel.demo', 'spiel.renderables', 'spiel.screens', 'spiel.widgets']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8', 'rich>=12', 'textual>=0.5', 'typer>=0.6', 'watchfiles>=0.18']

entry_points = \
{'console_scripts': ['spiel = spiel.cli:cli']}

setup_kwargs = {
    'name': 'spiel',
    'version': '0.4.0',
    'description': 'A framework for building and presenting richly-styled presentations in your terminal using Python.',
    'long_description': "# Spiel\n\n[![PyPI](https://img.shields.io/pypi/v/spiel)](https://pypi.org/project/spiel/)\n[![Documentation Status](https://readthedocs.org/projects/spiel/badge/?version=latest)](https://spiel.readthedocs.io/en/latest/?badge=latest)\n[![PyPI - License](https://img.shields.io/pypi/l/spiel)](https://pypi.org/project/spiel/)\n\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/JoshKarpel/spiel/main.svg)](https://results.pre-commit.ci/latest/github/JoshKarpel/spiel/main)\n[![codecov](https://codecov.io/gh/JoshKarpel/spiel/branch/main/graph/badge.svg?token=2sjP4V0AfY)](https://codecov.io/gh/JoshKarpel/spiel)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n[![GitHub issues](https://img.shields.io/github/issues/JoshKarpel/spiel)](https://github.com/JoshKarpel/spiel/issues)\n[![GitHub pull requests](https://img.shields.io/github/issues-pr/JoshKarpel/spiel)](https://github.com/JoshKarpel/spiel/pulls)\n\nSpiel is a framework for building and presenting richly-styled presentations in your terminal using Python.\n\nTo see what Spiel can do without installing it, you can view the demonstration deck in a container:\n```bash\n$ docker run -it --rm ghcr.io/joshkarpel/spiel\n```\nAlternatively, install Spiel (`pip install spiel`) and run this command to view the demonstration deck:\n```bash\n$ spiel demo present\n```\n\n## Sandboxed Execution via Containers\n\nSpiel presentations are live Python code: they can do anything that Python can do.\nYou may want to run untrusted presentations (or even your own presentations) inside a container (but remember, even containers are not perfectly safe!).\nWe produce a [container image](https://github.com/users/JoshKarpel/packages/container/package/spiel)\nthat can be run by (for example) Docker.\n\nPresentations without extra Python dependencies might just need to be bind-mounted into the container.\nFor example, if your demo file is at `$PWD/presentation/deck.py`, you could do\n```bash\n$ docker run -it --rm --mount type=bind,source=$PWD/presentation,target=/presentation ghcr.io/joshkarpel/spiel spiel present /presentation/deck.py\n```\n\nIf the presentation has extra dependencies (like other Python packages),\nwe recommend building a new image that inherits our image (e.g., `FROM ghcr.io/joshkarpel/spiel:vX.Y.Z`).\nSpiel's image itself inherits from the [Python base image](https://hub.docker.com/_/python).\n\n## Supported Systems\n\nSpiel currently relies on underlying terminal mechanisms that are only available on POSIX systems (e.g., Linux and MacOS).\nIf you're on Windows, you can use the [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/) to run Spiel.\n",
    'author': 'JoshKarpel',
    'author_email': 'josh.karpel@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/JoshKarpel/spiel',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4',
}


setup(**setup_kwargs)
