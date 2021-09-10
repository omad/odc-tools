import pytest
from click.testing import CliRunner
from pathlib import Path

from odc.apps.dc_tools.fs_to_dc import cli

TEST_DATA_FILE: Path = Path(__file__).parent / "data" / "NASADEM_HGT_s56w072.stac-item.json"


@pytest.mark.depends(on=["add_products"])
def test_fs_to_fc_yaml(test_data_dir):
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [test_data_dir, "--stac", str(TEST_DATA_FILE)],
    )
    assert result.exit_code == 0


@pytest.fixture
def test_data_dir():
    return str(TEST_DATA_FOLDER)
