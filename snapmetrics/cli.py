from typing import Optional

import typer

from snapmetrics import base

cli = typer.Typer(name=f"{base.NAME} CLI")


@cli.command()
def run(
    image_path: str = "./static/image.jpg",
    camera_name: Optional[str] = None,
    lens: Optional[str] = None,
    settings: Optional[str] = None,
    use_exif: bool = False,
    output_path: str = "./static/output_image_with_info.jpg",
    margin: int = 100,
    show_image: bool = True,
):  # pragma: no cover
    """Run snapmetrics CLI.

    Process an image and add camera and lens information.

    Args:
        image_path: Path to the input image file
        camera_name: Camera name to display
        lens: Lens information to display
        settings: Camera settings to display
        use_exif: Whether to use EXIF data from the image
        output_path: Path to save the processed image
        margin: Margin size in pixels
        show_image: Whether to display the output image
    """
    print("Start snapmetrics CLI")

    processor = base.ImageProcessor()

    if use_exif:
        print("Extracting EXIF data from image...")
        exif_data = processor.extract_exif(image_path)

        if camera_name is None:
            camera_name = exif_data["camera_name"]
            print(f"Using camera name from EXIF: {camera_name}")

        if lens is None:
            lens = exif_data["lens"]
            print(f"Using lens from EXIF: {lens}")

        if settings is None:
            settings = exif_data["settings"]
            print(f"Using settings from EXIF: {settings}")

    camera_name = camera_name or "Default Camera Name"
    lens = lens or "Default Lens Name"
    settings = settings or "Default Settings"

    print(f"Camera: {camera_name}")
    print(f"Lens: {lens}")
    print(f"Settings: {settings}")

    info = base.ImageInfo(camera=camera_name, lens=lens, settings=settings)
    result_image = processor.process_image(image_path, info, margin=margin)

    result_image.save(output_path)
    print(f"Image saved to {output_path}")

    if show_image:
        result_image.show()


if __name__ == "__main__":
    cli()
