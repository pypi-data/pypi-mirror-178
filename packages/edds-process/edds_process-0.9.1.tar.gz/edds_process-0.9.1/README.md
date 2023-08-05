edds_process
============

[![pipeline status](https://gitlab.obspm.fr/rpw/edds_process/badges/develop/pipeline.svg)](https://gitlab.obspm.fr/rpw/edds_process/pipelines)

Python Package to handle EGOS Data Dissemination System (EDDS) Data.

## Quickstart

To install package using [pip](https://pypi.org/project/pip-tools/):

```
pip install edds_process --extra-index-url https://__token__:<your_personal_token>@gitlab.obspm.fr/api/v4/projects/2052/packages/pypi/simple --trusted-host gitlab.obspm.fr
```

To install package from source files:

```
git clone https://gitlab.obspm.fr/rpw/edds_process.git
```

Then install using [pip](https://pypi.org/project/pip-tools/):

```
cd edds_proces
pip install .
```

or using [poetry](https://python-poetry.org/):

```
cd edds_process
pip install poetry
poetry install
```

## User guide

Package modules can be then imported into codes with line `import edds_process`.

Especially, `edds_process.response` module contains methods to parse/create TmRaw/TcReport EDDS XML files.

## Authors

- xavier dot bonnin at obspm dot fr
