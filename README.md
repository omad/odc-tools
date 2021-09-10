[![Test Status](https://github.com/opendatacube/odc-tools/actions/workflows/main.yml/badge.svg)](https://github.com/opendatacube/odc-tools/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/opendatacube/odc-tools/branch/develop/graph/badge.svg?token=PovpVLRFwn)](https://codecov.io/gh/opendatacube/odc-tools)

ODC Prototype Code
==================

This repository contains Open Datacube related libraries and command line tools
that are still under development, or too small to yet be released as their own
repository.


Contents
========

<!-- toc --> 
<!-- tocstop -->

Applications and Tools
======================

- [Datacube Statistician](libs/stats/) Dask based tool and library for generating statistical summaries of large collections of Earth Observation Imagery
- [Datacube Tools](apps/dc_tools/) Streamlined tools for working with Open Datacube indexes
- [Cloud Tools](apps/cloud/) Command line tools not specific to Open Datacube

Libraries
=========

- [Algorithms](libs/algo/) Algorithms and associated helper methods
- [Cloud](libs/cloud/) Functions for working with AWS, Azure and THREDDS
- [Dataset cache](libs/dscache/) High speed random access Dataset cache
- [IO](libs/io/) Common IO Utilities, used internally in the provided apps.
- [STAC](libs/stac/) Tools for converting between [STAC](https://stacspec.org/) and Open Datacube

Installation
============

This repository provides a number of [libraries](https://github.com/opendatacube/odc-tools/tree/develop/libs)
and [CLI tools](https://github.com/opendatacube/odc-tools/tree/develop/apps).

Full list of libraries, and install instructions:

- `odc.algo` algorithms (GeoMedian wrapper is here)
- `odc.stats` large scale processing framework (under development)
- `odc.ui` tools for data visualization in notebook/lab
- `odc.stac` STAC to ODC conversion tools
- `odc.dscache` experimental key-value store where `key=UUID`, `value=Dataset`
- `odc.io` common IO utilities, used by apps mainly
- `odc-cloud[ASYNC,AZURE,THREDDS]` cloud crawling support package
  - `odc.aws` AWS/S3 utilities, used by apps mainly
  - `odc.aio` faster concurrent fetching from S3 with async, used by apps `odc-cloud[ASYNC]`
  - `odc.{thredds,azure}` internal libs for cloud IO `odc-cloud[THREDDS,AZURE]`

Pre-release of these libraries is on PyPI now, so can be installed with `pip`
"the normal way". Most recent development versions of `odc-tools` packages are
pushed to `https://packages.dea.ga.gov.au`, and can be installed like so:

```
pip install --extra-index-url="https://packages.dea.ga.gov.au" \
  odc-ui \
  odc-stac \
  odc-stats \
  odc-algo \
  odc-io \
  odc-cloud[ASYNC] \
  odc-dscache
```

**NOTE**: on Ubuntu 18.04 the default `pip` version is awfully old and does not
support `--extra-index-url` command line option, so make sure to upgrade `pip`
first: `pip3 install --upgrade pip`.

For Conda Users
---------------

Currently there are no `odc-tools` conda packages. But the majority of `odc-tools`
dependencies can be installed with conda from the `conda-forge` channel.

Use `conda env update -f environment.yaml` to install all needed dependencies for
`odc-tools` libraries and apps.

See [environment.yaml](environment.yaml).

CLI Tools
=========

Installation
------------

The AWS cloud tools depend on the `aiobotocore` package which has a dependency on a specific
version of `botocore`. Another package we use, `boto3`, also depends on a
specific version of `botocore`. As a result having both `aiobotocore` and
`boto3` in one environment can be a bit tricky. The easiest way to solve this,
is to install `aiobotocore[awscli,boto3]` before anything else, which will pull
in a compatible version of `boto3` and `awscli` into the environment.

```
pip install -U "aiobotocore[awscli,boto3]==1.3.3"
# OR for conda setups
conda install "aiobotocore==1.3.3" boto3 awscli
```

The specific version of `aiobotocore` is not relevant, but it is needed in
practice to limit `pip`/`conda` package resolution search.


1. For cloud (AWS only)
   ```
   pip install odc-apps-cloud
   ```
2. For cloud (GCP, THREDDS and AWS)
   ```
   pip install odc-apps-cloud[GCP,THREDDS]
   ```
2. For `dc-index-from-tar` (indexing to datacube from tar archive)
   ```
   pip install odc-apps-dc-tools
   ```



Local Development
=================

Requires docker, procedure was only tested on Linux hosts.

```bash
docker pull opendatacube/odc-test-runner:latest

cd odc-tools
make -C docker run-test
```

Above will run tests and generate test coverage report in `htmlcov/index.html`.

Other option is to run `make -C docker bash`, this will drop you into a shell in
`/code` folder that contains your current checkout of `odc-tools`. You can then
use `with-test-db start` command to launch and setup test database for running
integration tests that require datacube database to work. From here on you can
run specific tests you are developing with `py.test ./path/to/test_file.py`. Any
changes you make to code outside of the docker environment are available without
any further action from you for testing.


Release Process
===============

Development versions of packages are pushed to [DEA packages
repo](https://packages.dea.ga.gov.au/) on every push to `develop` branch,
version is automatically increased by a script that runs before creating wheels
and source distribution tar balls. Right now new dev version is pushed for all
the packages even the ones that have not changed since last push.

Publishing to [PyPi](https://pypi.org/) happens automatically when changes are
pushed to a protected `pypi/publish` branch. Only members of [Open Datacube
Admins](https://github.com/orgs/opendatacube/teams/admins) group have the
permission to push to this branch.

Process:

1. Manually edit `{lib,app}/{pkg}/odc/{pkg}/_version.py` file to increase version number
2. Merge it to `develop` branch via PR
3. Fast forward `pypi/publish` branch to match `develop`
4. Push it to GitHub

Steps 3 and 4 can be done by an authorized user with
`./scripts/sync-publish-branch.sh` script.
