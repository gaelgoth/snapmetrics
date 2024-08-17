import pytest

given = pytest.mark.parametrize


def test_help(cli_client, cli):
    result = cli_client.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Run snapmetrics CLI." in result.stdout


# See example:
# https://github.com/rochacbruno/fastapi-project-template/blob/main/tests/conftest.py
