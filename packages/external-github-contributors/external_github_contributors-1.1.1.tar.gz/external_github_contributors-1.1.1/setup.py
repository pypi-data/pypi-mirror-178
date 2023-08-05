# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['external_github_contributors']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['external_github_contributors = '
                     'external_github_contributors:main']}

setup_kwargs = {
    'name': 'external-github-contributors',
    'version': '1.1.1',
    'description': 'Simple script to list external contributors to a project who authored contributions between two specific references',
    'long_description': "# External GitHub contributors\n\nThis is a simple script to get a list of external contributors that authored commits on a\nGitHub-hosted project within a range defined by two given Git references.\n\n## Install\n\nThis project can be installed via `pip`:\n\n```commandline\npip install external-github-contributors\n```\n\n### Install from source\n\nThis project uses [Poetry](https://python-poetry.org/) to manage its dependencies. Poetry\nneeds to be installed in order to be able to follow the installation and usage\ninstructions.\n\nClone the repository and install the dependencies:\n\n```commandline\ngit clone https://github.com/babolivier/external-github-contributors.git\ncd external-github-contributors\npoetry install\n```\n\n## Usage\n\nIf you have installed this project using `pip`, run `python -m external_github_contributors`.\n\nIf you have installed this project from source, in your local checkout of this repository,\nrun `poetry run external_github_contributors [args]`.\n\nA complete synopsis is available below:\n\n```\nusage: external_github_contributors [-h] --team TEAM --repo REPO [--token TOKEN] [--md] oldest_ref most_recent_ref\n\nSimple script to list external contributors to a project who authored contributions between two specific references.\n\npositional arguments:\n  oldest_ref       The oldest of the two refs to compare.\n  most_recent_ref  The most recent of the two refs to compare.\n\noptions:\n  -h, --help       show this help message and exit\n  --team TEAM      The team listing internal contributors to exclude. In the format ORG_NAME/teams/TEAM_SLUG.\n  --repo REPO      The repository to list contributors of. In the format ORG_NAME/REPO_NAME.\n  --token TOKEN    The GitHub access token to use when making request to the API. Must have the read:org scope.\n                   If not provided as a command-line argument, must be in the GITHUB_TOKEN environment variable.\n  --md             If provided, prints the contributors as markdown links. The text for the link is the user's\n                   display name (e.g. full name) as configured in their GitHub profile. This option requires an\n                   additional API call for each contributor, and therefore introduces additional delay.\n```\n\nAs an example, here's a run of the script to get the list of external contributors that\ncommitted to the [matrix-org/synapse](https://github.com/matrix-org/synapse) repository\nbetween Synapse 1.68 and Synapse 1.69:\n\n```\npython -m external_github_contributors --team=matrix-org/teams/core-team --repo=matrix-org/synapse v1.68.0 v1.69.0\n10 external contributors found after looking at 114 commits:\n- ...\n```\n\nIn this example, the GitHub access token is stored in the environment.\n\n## Contribute\n\nPlease report bugs as issues on this repository, although fixing them will be done on a\nbest-effort basis. Pull requests are welcome.\n",
    'author': 'Brendan Abolivier',
    'author_email': 'hello@brendanabolivier.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
