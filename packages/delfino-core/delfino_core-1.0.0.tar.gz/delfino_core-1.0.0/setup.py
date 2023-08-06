# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['delfino_core']

package_data = \
{'': ['*']}

install_requires = \
['delfino[verify-all]>=0.20.3,<0.21.0']

entry_points = \
{'delfino.plugin': ['delfino-core = delfino_core']}

setup_kwargs = {
    'name': 'delfino-core',
    'version': '1.0.0',
    'description': 'Delfino core plugin',
    'long_description': '<h1 align="center" style="border-bottom: none;"> 🔌&nbsp;&nbsp;Delfino Core&nbsp;&nbsp; 🔌</h1>\n<h3 align="center">A [Delfino](https://github.com/radeklat/delfino) plugin with core functionality.</h3>\n\n<p align="center">\n    <a href="https://app.circleci.com/pipelines/github/radeklat/delfino-core?branch=main">\n        <img alt="CircleCI" src="https://img.shields.io/circleci/build/github/radeklat/delfino-core">\n    </a>\n    <a href="https://app.codecov.io/gh/radeklat/delfino-core/">\n        <img alt="Codecov" src="https://img.shields.io/codecov/c/github/radeklat/delfino-core">\n    </a>\n    <a href="https://github.com/radeklat/delfino-core/tags">\n        <img alt="GitHub tag (latest SemVer)" src="https://img.shields.io/github/tag/radeklat/delfino-core">\n    </a>\n    <img alt="Maintenance" src="https://img.shields.io/maintenance/yes/2022">\n    <a href="https://github.com/radeklat/delfino-core/commits/main">\n        <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/radeklat/delfino-core">\n    </a>\n    <a href="https://www.python.org/doc/versions/">\n        <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/delfino-core">\n    </a>\n    <a href="https://pypistats.org/packages/delfino-core">\n        <img alt="Downloads" src="https://img.shields.io/pypi/dm/delfino-core">\n    </a>\n</p>\n\n# Installation\n\n- pip: `pip install delfino-core`\n- Poetry: `poetry add -D delfino-core`\n- Pipenv: `pipenv install -d delfino-core`\n\n## Configuration\n\nDelfino doesn\'t load any plugins by default. To enable this plugin, add the following config into `pyproject.toml`:\n\n```toml\n[tool.delfino.plugins.delfino-core]\n\n```\n\n# Usage\n\nRun `delfino --help`.\n',
    'author': 'Radek Lát',
    'author_email': 'radek.lat@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/radeklat/delfino-core',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
