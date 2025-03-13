from unittest.mock import MagicMock, patch

import pytest

given = pytest.mark.parametrize


def test_help(cli_client, cli):
    result = cli_client.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Run snapmetrics CLI." in result.stdout
    assert "--use-exif" in result.stdout
    assert "--image-path" in result.stdout
    assert "--output-path" in result.stdout


@pytest.mark.parametrize(
    "params, expected_outputs",
    [
        (
            [],
            [
                "Camera: Default Camera Name",
                "Lens: Default Lens Name",
                "Settings: Default Settings",
            ],
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
            ["Camera: SONY A7C", "Lens: 18-55mm", "Settings: ISO 200, f/5.6"],
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
            ["Camera: Canon AF35M", "Lens: 38mm 1:28", "Settings: Kodak Ultra Max 400"],
        ),
        (
            ["--camera-name", "Fujifilm X100V"],
            [
                "Camera: Fujifilm X100V",
                "Lens: Default Lens Name",
                "Settings: Default Settings",
            ],
        ),
        (
            ["--image-path", "./test_image.jpg", "--output-path", "./test_output.jpg"],
            ["Image saved to ./test_output.jpg"],
        ),
        (
            ["--no-show-image"],
            ["Image saved to"],
        ),
    ],
)
def test_cli_params(cli_client, cli, params, expected_outputs):
    """Test various combinations of CLI parameters."""
    with patch("snapmetrics.base.ImageProcessor.process_image") as mock_process_image:
        # Mock the process_image method to return a mock image
        mock_image = MagicMock()
        mock_process_image.return_value = mock_image

        result = cli_client.invoke(cli, params)

        assert result.exit_code == 0
        for expected in expected_outputs:
            assert expected in result.stdout
        assert "Start snapmetrics CLI" in result.stdout

        # Verify that process_image was called
        mock_process_image.assert_called_once()
        # Verify that save was called on the mock image
        mock_image.save.assert_called_once()

        # If --no-show-image is used, show should not be called
        if "--no-show-image" in params:
            mock_image.show.assert_not_called()
        else:
            mock_image.show.assert_called_once()


@pytest.mark.parametrize(
    "use_exif, camera_provided, lens_provided, settings_provided, exif_data",
    [
        # Use EXIF for all fields
        (
            True,
            False,
            False,
            False,
            {
                "camera_name": "SONY A7IV",
                "lens": "24-70mm f/2.8",
                "settings": "f/2.8, 1/60s, ISO 100",
            },
        ),
        # Use EXIF for lens and settings only
        (
            True,
            True,
            False,
            False,
            {
                "camera_name": "SONY A7IV",
                "lens": "24-70mm f/2.8",
                "settings": "f/2.8, 1/60s, ISO 100",
            },
        ),
        # Use EXIF for camera only
        (
            True,
            False,
            True,
            True,
            {
                "camera_name": "SONY A7IV",
                "lens": "24-70mm f/2.8",
                "settings": "f/2.8, 1/60s, ISO 100",
            },
        ),
        # Don't use EXIF even if flag is provided but no data available
        (
            True,
            False,
            False,
            False,
            {
                "camera_name": "No EXIF data",
                "lens": "No EXIF data",
                "settings": "No EXIF data",
            },
        ),
    ],
)
def test_exif_usage(
    cli_client,
    cli,
    use_exif,
    camera_provided,
    lens_provided,
    settings_provided,
    exif_data,
):
    """Test EXIF data extraction functionality."""
    with patch(
        "snapmetrics.base.ImageProcessor.extract_exif"
    ) as mock_extract_exif, patch(
        "snapmetrics.base.ImageProcessor.process_image"
    ) as mock_process_image:

        # Mock EXIF extraction
        mock_extract_exif.return_value = exif_data

        # Set up mock for process_image
        mock_image = MagicMock()
        mock_process_image.return_value = mock_image

        # Prepare parameters based on test case
        params = []
        if use_exif:
            params.append("--use-exif")
        if camera_provided:
            params.extend(["--camera-name", "Custom Camera"])
        if lens_provided:
            params.extend(["--lens", "Custom Lens"])
        if settings_provided:
            params.extend(["--settings", "Custom Settings"])

        # Run CLI command
        result = cli_client.invoke(cli, params)

        # Verify results
        assert result.exit_code == 0

        # Verify EXIF extraction was called only if use_exif is True
        if use_exif:
            mock_extract_exif.assert_called_once()
            assert "Extracting EXIF data from image..." in result.stdout

            # Check which values were used based on provided parameters and EXIF data
            if camera_provided:
                assert "Camera: Custom Camera" in result.stdout
            else:
                assert f"Camera: {exif_data['camera_name']}" in result.stdout
                if exif_data["camera_name"] != "No EXIF data":
                    assert (
                        f"Using camera name from EXIF: {exif_data['camera_name']}"
                        in result.stdout
                    )

            if lens_provided:
                assert "Lens: Custom Lens" in result.stdout
            else:
                assert f"Lens: {exif_data['lens']}" in result.stdout
                if exif_data["lens"] != "No EXIF data":
                    assert f"Using lens from EXIF: {exif_data['lens']}" in result.stdout

            if settings_provided:
                assert "Settings: Custom Settings" in result.stdout
            else:
                assert f"Settings: {exif_data['settings']}" in result.stdout
                if exif_data["settings"] != "No EXIF data":
                    assert (
                        f"Using settings from EXIF: {exif_data['settings']}"
                        in result.stdout
                    )
        else:
            mock_extract_exif.assert_not_called()

        mock_process_image.assert_called_once()


# See example:
# https://github.com/rochacbruno/fastapi-project-template/blob/main/tests/conftest.py
