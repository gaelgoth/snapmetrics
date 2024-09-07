"""CLI interface for snapmetrics project.

Be creative! do whatever you want!

- Install click or typer and create a CLI app
- Use builtin argparse
- Start a web application
- Import things from your .base module
"""

import typer

from snapmetrics import base

cli = typer.Typer(name=f"{base.NAME} CLI")


@cli.command()
def run(
    camera_name: str = "Default Camera Name",
    lens: str = "Default lens Name",
    settings: str = "Default settings",
):  # pragma: no cover
    """Run snapmetrics CLI."""
    print("Start snapmetrics CLI")

    print(f"--camera-name is {camera_name}, --lens is {lens}, --settings is {settings}")

    # font_path = "./static/JetBrainsMonoNerdFontMono-Regular"
    processor = base.ImageProcessor()
    # TODO: Handle default values
    # TODO: Read image EXIF
    info = base.ImageInfo(camera=camera_name, lens=lens, settings=settings)

    result_image = processor.process_image("./static/image.jpg", info, margin=100)

    result_image.save("./static/output_image_with_info.jpg")
    result_image.show()
