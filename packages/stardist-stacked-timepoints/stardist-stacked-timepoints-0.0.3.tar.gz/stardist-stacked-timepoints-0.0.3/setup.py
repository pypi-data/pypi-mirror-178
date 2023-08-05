# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['stardist_stacked_timepoints']

package_data = \
{'': ['*']}

install_requires = \
['edt>=2.3.0,<3.0.0',
 'numpy>=1.20.0',
 'scipy>=1.9.3,<2.0.0',
 'stardist>=0.8.3,<0.9.0']

entry_points = \
{'console_scripts': ['stardist-stacked-timepoints = '
                     'stardist_stacked_timepoints.__main__:main']}

setup_kwargs = {
    'name': 'stardist-stacked-timepoints',
    'version': '0.0.3',
    'description': 'Stardist Stacked Timepoints',
    'long_description': "# Stardist Stacked Timepoints\n\n[![PyPI](https://img.shields.io/pypi/v/stardist-stacked-timepoints.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/stardist-stacked-timepoints.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/stardist-stacked-timepoints)][python version]\n[![License](https://img.shields.io/pypi/l/stardist-stacked-timepoints)][license]\n\n[![Read the documentation at https://stardist-stacked-timepoints.readthedocs.io/](https://img.shields.io/readthedocs/stardist-stacked-timepoints/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/gatoniel/stardist-stacked-timepoints/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/gatoniel/stardist-stacked-timepoints/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/stardist-stacked-timepoints/\n[status]: https://pypi.org/project/stardist-stacked-timepoints/\n[python version]: https://pypi.org/project/stardist-stacked-timepoints\n[read the docs]: https://stardist-stacked-timepoints.readthedocs.io/\n[tests]: https://github.com/gatoniel/stardist-stacked-timepoints/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/gatoniel/stardist-stacked-timepoints\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n## Features\n\n- TODO\n\n## Requirements\n\n- TODO\n\n## Installation\n\nYou can install _Stardist Stacked Timepoints_ via [pip] from [PyPI]:\n\n```console\n$ pip install stardist-stacked-timepoints\n```\n\n## Usage\n\nPlease see the [Command-line Reference] for details.\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_Stardist Stacked Timepoints_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/gatoniel/stardist-stacked-timepoints/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/gatoniel/stardist-stacked-timepoints/blob/main/LICENSE\n[contributor guide]: https://github.com/gatoniel/stardist-stacked-timepoints/blob/main/CONTRIBUTING.md\n[command-line reference]: https://stardist-stacked-timepoints.readthedocs.io/en/latest/usage.html\n",
    'author': 'Niklas Netter',
    'author_email': 'niknett@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gatoniel/stardist-stacked-timepoints',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
