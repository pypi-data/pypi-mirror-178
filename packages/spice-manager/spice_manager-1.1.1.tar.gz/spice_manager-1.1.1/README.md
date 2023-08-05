
spice_manager
=============

[![pipeline status](https://gitlab.obspm.fr/rpw/spice_manager/badges/develop/pipeline.svg)](https://gitlab.obspm.fr/rpw/spice_manager/pipelines)

Program to deal with NAIF SPICE kernels for Solar Orbiter (see https://www.cosmos.esa.int/web/spice/solar_orbiter for more details).

spice_manager relies on the *spiceypy* Python package (https://pypi.org/project/spiceypy/).

## Quickstart

To install package using [pip](https://pypi.org/project/pip-tools/):

```
pip install spice_manager --extra-index-url https://__token__:<your_personal_token>@gitlab.obspm.fr/api/v4/projects/2052/packages/pypi/simple --trusted-host gitlab.obspm.fr
```

To install package from source files:

```
git clone https://gitlab.obspm.fr/rpw/spice_manager.git
```

Then install using [pip](https://pypi.org/project/pip-tools/):

```
cd spice_manager
pip install .
```

or using [poetry](https://python-poetry.org/):

```
cd spice_manager
pip install poetry
poetry install
```

## User guide

Package modules can be then imported into codes with line `import spice_manager`.

Especially `spice_manager.SpiceManager` class contains methods to handle SPICE Kernels and some time conversions.

## Authors

- xavier dot bonnin at obspm dot fr
