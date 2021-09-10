"""
fs-to-dc allows adding datasets stored on the filesystem to an ODC Index

It improves upon `datacube dataset add` and `datacube dataset update` in several ways
- Automatically choose whether to Add or Update a dataset
- Allow indexing STAC format
"""
import click
import logging
import yaml
from odc.stac.transform import stac_transform

import datacube
from datacube.index.hl import Doc2Dataset
from odc.apps.dc_tools.utils import (
    index_update_dataset,
    update_if_exists,
    allow_unsafe,
    transform_stac,
)
from odc.stac.transform import stac_transform
from typing import Generator, Optional
import logging


import yaml
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s: %(levelname)s: %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S",
)


def _find_files(
    path: str, glob: Optional[str] = None, stac: Optional[bool] = False
) -> Generator[Path, None, None]:
    if glob is None:
        glob = "**/*.json" if stac else "**/*.yaml"

def setup_logging()
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s: %(levelname)s: %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S",
    )


@click.command("fs-to-dc",
               help=__doc__)
@click.argument("DATASET_FILES", type=str, nargs=-1)
@update_if_exists
@allow_unsafe
@transform_stac
def cli(dataset_files, update_if_exists, allow_unsafe, stac):
    dc = datacube.Datacube()
    doc2ds = Doc2Dataset(dc.index)

    if glob is None:
        glob = "**/*.json" if stac else "**/*.yaml"

    files_to_process = _find_files(input_directory, glob, stac=stac)

    added, failed = 0, 0

    for in_file in dataset_files:
        with in_file.open() as f:
            try:
                if in_file.endswith(".yml") or in_file.endswith(".yaml"):
                    metadata = yaml.safe_load(f, Loader=Loader)
                else:
                    metadata = json.load(f)
                # Do the STAC Transform if it's flagged
                if stac:
                    metadata = stac_transform(metadata)
                index_update_dataset(
                    metadata,
                    in_file.absolute().as_uri(),
                    dc=dc,
                    doc2ds=doc2ds,
                    update_if_exists=update_if_exists,
                    allow_unsafe=allow_unsafe,
                )
                added += 1
            except Exception as e:
                logging.exception(f"Failed to add dataset {in_file} with error {e}")
                failed += 1

    logging.info(f"Added {added} and failed {failed} datasets.")


if __name__ == "__main__":
    setup_logging()
    cli()
