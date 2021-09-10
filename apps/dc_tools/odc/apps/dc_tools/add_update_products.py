"""
Add or update a list of ODC products.

Synchronises a CSV list of products with an ODC Database

The format of the CSV is:

    name,definition

For example:

    name,definition
    ls8_sr,https://raw.githubusercontent.com/digitalearthafrica/config/master/products/ls8_sr.odc-product.yaml
    gm_s2_annual,https://raw.githubusercontent.com/digitalearthafrica/config/master/products/gm_s2_annual.odc-product.yaml

For cases when a single YAML file contains multiple product definitions, the `name` must
contain a ; separated list of product names.
"""

from collections import Counter, namedtuple

import click
import fsspec
import logging
import sys
import yaml
from csv import DictReader
from typing import Any, Dict, List, Tuple
from typing import Optional

import datacube
from datacube import Datacube
from odc.apps.dc_tools.utils import update_if_exists

Product = namedtuple('Product', ['name', 'doc'])


def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S')


def _get_product(product_path: str) -> List[Dict[str, Any]]:
    """Loads a YAML document from a URL"""
    try:
        with fsspec.open(product_path, mode="r") as f:
            return [d for d in yaml.safe_load_all(f)]
    except Exception as e:
        logging.error(f"Failed to get document from {product_path} with exception: {e}")
        return []


def _parse_csv(csv_path: str) -> Dict[str, str]:
    """Parses the CSV and returns a dict of name: yaml_file_path"""

    with fsspec.open(csv_path, mode="r") as f:
        reader = DictReader(f)
        for row in reader:
            names = row["product"].split(";")
            content = _get_product(row["definition"])

            # Do some QA

            # Check we have the same number of names as content
            if len(names) != len(content):
                logging.error(f"{len(names)} product names and {len(content)} documents found. This is different!")
                yield Product(row["product"], None)
                continue

            # Check we have the same names as are in the product definitions
            content_names = [d["name"] for d in content]
            if not set(content_names) == set(names):
                logging.error(f"{names} is not the same as {content_names}")
                yield Product(row["product"], None)
                continue

            # There's only one name in names, so yield it
            if len(names) == 1:
                yield Product(names[0], content[0])
            else:
                # Handle multiple documents in a single file
                for doc in content:
                    # Since we checked all the names, we can do this safely
                    yield Product(doc["name"], doc)


def add_update_products(
        dc: Datacube, csv_path: str, update_if_exists: Optional[bool] = False
) -> Tuple[int, int, int]:
    # Parse csv file
    new_products = [x for x in _parse_csv(csv_path)]
    logging.info(f"Found {len(new_products)} products in the CSV {csv_path}")

    # List existing products
    products = dc.list_products(with_pandas=False)
    existing_names = [product["name"] for product in products]
    logging.info(f"Found {len(existing_names)} products in the Datacube")

    added, updated, failed = 0, 0, 0

    for product in new_products:
        if product.doc is None:
            failed += 1
            continue
        # Add new products
        try:
            if product.name not in existing_names:
                dc.index.products.add_document(product.doc)
                added += 1
                logging.info(f"Added product {product.name}")
            # Update existing products, if required
            elif update_if_exists:
                dc.index.products.update_document(
                    product.doc, allow_unsafe_updates=True
                )
                updated += 1
                logging.info(f"Updated product {product.name}")
        except Exception as e:
            failed += 1
            logging.error(f"Failed to add/update product {product.name} with exception: {e}")

    # Return results
    return added, updated, failed


@click.command("dc-sync-products", help=__doc__)
@click.argument("csv-path", nargs=1)
@update_if_exists
def cli(csv_path: str, update_if_exists: bool):
    # Check we can connect to the Datacube
    dc = datacube.Datacube(app="add_update_products")
    logging.info(f"Starting up: connected to Datacube, and update-if-exists is {update_if_exists}")

    # TODO: Add in some QA/QC checks
    added, updated, failed = add_update_products(dc, csv_path, update_if_exists)

    print(f"Added: {added}, Updated: {updated} and Failed: {failed}")

    # If nothing failed then this exists with success code 0
    sys.exit(failed)


if __name__ == "__main__":
    setup_logging()
    cli()
