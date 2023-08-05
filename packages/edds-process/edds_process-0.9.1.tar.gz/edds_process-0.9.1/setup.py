# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['edds_process', 'edds_process.request', 'edds_process.response']

package_data = \
{'': ['*']}

install_requires = \
['xmltodict>=0.13,<0.14']

setup_kwargs = {
    'name': 'edds-process',
    'version': '0.9.1',
    'description': 'Package to process data from the EGOS Data Dissemination System (EDDS) of ESA',
    'long_description': 'edds_process\n============\n\n[![pipeline status](https://gitlab.obspm.fr/rpw/edds_process/badges/develop/pipeline.svg)](https://gitlab.obspm.fr/rpw/edds_process/pipelines)\n\nPython Package to handle EGOS Data Dissemination System (EDDS) Data.\n\n## Quickstart\n\nTo install package using [pip](https://pypi.org/project/pip-tools/):\n\n```\npip install edds_process --extra-index-url https://__token__:<your_personal_token>@gitlab.obspm.fr/api/v4/projects/2052/packages/pypi/simple --trusted-host gitlab.obspm.fr\n```\n\nTo install package from source files:\n\n```\ngit clone https://gitlab.obspm.fr/rpw/edds_process.git\n```\n\nThen install using [pip](https://pypi.org/project/pip-tools/):\n\n```\ncd edds_proces\npip install .\n```\n\nor using [poetry](https://python-poetry.org/):\n\n```\ncd edds_process\npip install poetry\npoetry install\n```\n\n## User guide\n\nPackage modules can be then imported into codes with line `import edds_process`.\n\nEspecially, `edds_process.response` module contains methods to parse/create TmRaw/TcReport EDDS XML files.\n\n## Authors\n\n- xavier dot bonnin at obspm dot fr\n',
    'author': 'Xavier Bonnin',
    'author_email': 'xavier.bonnin@obspm.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.obspm.fr/ROC_PUBLIC/edds_process',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
