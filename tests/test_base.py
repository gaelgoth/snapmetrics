import pytest
from PIL import Image

from snapmetrics.base import NAME, Dimensions, ImageInfo, ImageProcessor


def test_base():
    assert NAME == "snapmetrics"


@pytest.fixture
def image_processor():
    return ImageProcessor("path/to/test/font.ttf")


def test_image_processor_init(image_processor):
    assert isinstance(image_processor, ImageProcessor)
    assert image_processor.font_path == "path/to/test/font.ttf"

    assert isinstance(image_processor.dimensions, Dimensions)
    assert image_processor.dimensions.width == 1080
    assert image_processor.dimensions.height == 1920


def test_create_base_image(image_processor):
    base_image = image_processor._create_base_image()
    assert isinstance(base_image, Image.Image)
    assert base_image.size == (1080, 1920)
    assert base_image.mode == "RGB"


def test_resize_original_image(image_processor):
    original_image = Image.new("RGB", (2000, 3000))
    resized_image = image_processor._resize_original_image(original_image)
    assert isinstance(resized_image, Image.Image)
    assert resized_image.size[0] <= 1080
    assert resized_image.size[1] <= 1920 * 0.7


def test_calculate_image_position(image_processor):
    resized_image = Image.new("RGB", (800, 1200))
    position = image_processor._calculate_image_position(resized_image)
    assert isinstance(position, tuple)
    assert len(position) == 2
    assert 0 <= position[0] <= 1080
    assert 0 <= position[1] <= 1920


@pytest.mark.parametrize("palette_size", [3, 5, 7])
def test_calculate_palette_config(image_processor, palette_size):
    image_position = (100, 100)
    image_height = 1000
    margin = 20
    config = image_processor._calculate_palette_config(
        palette_size, image_position, image_height, margin
    )
    assert isinstance(config, dict)
    assert "square_size" in config
    assert "start_x" in config
    assert "y" in config
    assert config["y"] == image_position[1] + image_height + margin


def test_image_info():
    info = ImageInfo(camera="Test Camera", lens="Test Lens", settings="Test Settings")
    assert info.camera == "Test Camera"
    assert info.lens == "Test Lens"
    assert info.settings == "Test Settings"
