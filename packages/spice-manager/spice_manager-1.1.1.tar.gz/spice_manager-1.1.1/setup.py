# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spice_manager']

package_data = \
{'': ['*']}

install_requires = \
['spiceypy>=5.1,<6.0']

setup_kwargs = {
    'name': 'spice-manager',
    'version': '1.1.1',
    'description': 'Package to deal with Solar Orbiter SPICE kernels',
    'long_description': '\nspice_manager\n=============\n\n[![pipeline status](https://gitlab.obspm.fr/rpw/spice_manager/badges/develop/pipeline.svg)](https://gitlab.obspm.fr/rpw/spice_manager/pipelines)\n\nProgram to deal with NAIF SPICE kernels for Solar Orbiter (see https://www.cosmos.esa.int/web/spice/solar_orbiter for more details).\n\nspice_manager relies on the *spiceypy* Python package (https://pypi.org/project/spiceypy/).\n\n## Quickstart\n\nTo install package using [pip](https://pypi.org/project/pip-tools/):\n\n```\npip install spice_manager --extra-index-url https://__token__:<your_personal_token>@gitlab.obspm.fr/api/v4/projects/2052/packages/pypi/simple --trusted-host gitlab.obspm.fr\n```\n\nTo install package from source files:\n\n```\ngit clone https://gitlab.obspm.fr/rpw/spice_manager.git\n```\n\nThen install using [pip](https://pypi.org/project/pip-tools/):\n\n```\ncd spice_manager\npip install .\n```\n\nor using [poetry](https://python-poetry.org/):\n\n```\ncd spice_manager\npip install poetry\npoetry install\n```\n\n## User guide\n\nPackage modules can be then imported into codes with line `import spice_manager`.\n\nEspecially `spice_manager.SpiceManager` class contains methods to handle SPICE Kernels and some time conversions.\n\n## Authors\n\n- xavier dot bonnin at obspm dot fr\n',
    'author': 'Xavier Bonnin',
    'author_email': 'xavier.bonnin@obspm.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.obspm.fr/ROC_PUBLIC/spice_manager',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
