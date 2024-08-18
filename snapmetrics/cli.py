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
def run():
    """Run snapmetrics CLI."""
    print("Test CLI")


@cli.command()
def produce_image():  # pragma: no cover
    print("Start Colorgram")

    # font_path = "./static/JetBrainsMonoNerdFontMono-Regular"
    processor = base.ImageProcessor()

    info = base.ImageInfo(
        camera="Canon AF35M", lens="38mm 1:28", settings="Kodak 400 Ultra Max"
    )

    result_image = processor.process_image("./static/image.jpg", info, margin=100)

    result_image.save("./static/output_image_with_info.jpg")
    result_image.show()
