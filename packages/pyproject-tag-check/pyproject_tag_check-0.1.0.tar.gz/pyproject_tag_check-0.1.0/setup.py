# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyproject_tag_check']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.10.0', 'toml>=0.9.0']

entry_points = \
{'console_scripts': ['pyproject-tag-check = pyproject_tag_check.__init__:main']}

setup_kwargs = {
    'name': 'pyproject-tag-check',
    'version': '0.1.0',
    'description': 'Verify version in pyproject.toml is not already used',
    'long_description': '## pyproject-tag-check\n\nI always forget to bump poetry version in pyproject.toml files. That\'s why I build this simple package. It is pre-commit hook which check that version in pyproject.toml is not used as a tag for given repo URL.\n\n## Usage:\n\n\nPut it in `.pre-commit.config.yaml` repos and argument must be URL to repo on GH (for example https://github.com/rafsaf/Tribal-Wars-Planer).\n\n```yml\nrepos:\n  - repo: https://github.com/rafsaf/pyproject-tag-check\n    rev: "0.1.0"\n    hooks:\n      - id: pyproject-tag-check\n        args:\n          - https://github.com/rafsaf/Tribal-Wars-Planer\n\n```\n',
    'author': 'rafsaf',
    'author_email': 'rafal.safin12@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
