from unittest.mock import patch

import pytest

given = pytest.mark.parametrize


def test_help(cli_client, cli):
    result = cli_client.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Run snapmetrics CLI." in result.stdout


@pytest.mark.parametrize(
    "params, expected_output",
    [
        # Testing no custom values (defaults should be used)
        (
            [],
            "--camera-name is Default Camera Name, --lens is Default lens Name, --settings is Default settings",
        ),
        # Testing different values for --camera-name, --lens, and --settings
        (
            [
                "--camera-name",
                "SONY A7C",
                "--lens",
                "18-55mm",
                "--settings",
                "ISO 200, f/5.6",
            ],
            "--camera-name is SONY A7C, --lens is 18-55mm, --settings is ISO 200, f/5.6",
        ),
        (
            [
                "--camera-name",
                "Canon AF35M",
                "--lens",
                "38mm 1:28",
                "--settings",
                "Kodak Ultra Max 400",
            ],
            "--camera-name is Canon AF35M, --lens is 38mm 1:28, --settings is Kodak Ultra Max 400",
        ),
        (
            ["--camera-name", "Fujifilm X100V"],
            "--camera-name is Fujifilm X100V, --lens is Default lens Name, --settings is Default settings",
        ),
    ],
)
def test_cli_params(cli_client, cli, params, expected_output):
    """Test various combinations of --camera-name, --lens, and --settings."""
    with patch("snapmetrics.base.ImageProcessor.process_image") as mock_process_image:

        # Mock the process_image method to return a mock image
        mock_process_image.return_value.save.return_value = None
        mock_process_image.return_value.show.return_value = None

        result = cli_client.invoke(cli, params)

        assert result.exit_code == 0
        assert expected_output in result.stdout
        # assert "Start snapmetrics CLI" in result.stdout

        # Verify that process_image was called
        mock_process_image.assert_called_once()


# See example:
# https://github.com/rochacbruno/fastapi-project-template/blob/main/tests/conftest.py
