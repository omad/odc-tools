# odc.apps.cloud

[up to odc-tools](../../)

Command line utilities for working with cloud "objects/files"


## Installation

```
pip install odc-apps-cloud
```

## Usage

1. `s3-find` list S3 bucket with wildcard
2. `s3-to-tar` fetch documents from S3 and dump them to a tar archive
3. `gs-to-tar` search Google Cloud Storage for documents and dump them to a tar archive


Example:


Fastest way to list regularly placed files is to use fixed depth listing:

```bash
#!/bin/bash

# only works when your metadata is same depth and has fixed file name
s3_src='s3://dea-public-data/L2/sentinel-2-nrt/S2MSIARD/*/*/ARD-METADATA.yaml'

s3-find --skip-check "${s3_src}" | \
  s3-to-tar | \
    dc-index-from-tar --env s2 --ignore-lineage
```

When using Google Storage:

```bash
#!/bin/bash

# Google Storage support
gs-to-tar --bucket data.deadev.com --prefix mangrove_cover
dc-index-from-tar --protocol gs --env mangroves --ignore-lineage metadata.tar.gz
```
- thredds-to-tar
- gs-to-tar
- s3-to-tar
- azure-to-tar


- s3-find
- s3-inventory-dump
- redrive-queue

1. `s3-find` list S3 bucket with wildcard
2. `s3-to-tar` fetch documents from S3 and dump them to a tar archive


Supported S3 Globs
------------------

`s3://dea-public-data/L2/sentinel-2-nrt/S2MSIARD/*/*/ARD-METADATA.yaml`

`s3://dea-public-data/L2/sentinel-2-nrt/**/*.yaml`
