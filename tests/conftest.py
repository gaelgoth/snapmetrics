import sys

import pytest
from typer.testing import CliRunner

from snapmetrics.cli import cli


# each test runs on cwd to its temp dir
@pytest.fixture(autouse=True)
def go_to_tmpdir(request):
    # Get the fixture dynamically by its name.
    tmpdir = request.getfixturevalue("tmpdir")
    # ensure local test created packages can be imported
    sys.path.insert(0, str(tmpdir))
    # Chdir only for the duration of the test.
    with tmpdir.as_cwd():
        yield


@pytest.fixture(scope="function", name="cli")
def _cli():
    return cli


@pytest.fixture(scope="function")
def cli_client():
    return CliRunner()
