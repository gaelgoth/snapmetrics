"""
snapmetrics base module.

This is the principal module of the snapmetrics project.
"""

from dataclasses import dataclass
from typing import List, Tuple

from PIL import Image, ImageDraw, ImageFont
from PIL.Image import Resampling
from Pylette import extract_colors

NAME = "snapmetrics"


@dataclass
class ImageInfo:
    camera: str
    lens: str
    settings: str


@dataclass
class Dimensions:
    width: int
    height: int


class ImageProcessor:
    def __init__(self, font_path: str):
        self.font_path = font_path
        self.dimensions = Dimensions(1080, 1920)

    def process_image(
        self,
        image_path: str,
        info: ImageInfo,
        palette_size: int = 5,
        margin: int = 20,
    ) -> Image.Image:
        palette = self._extract_palette(image_path, palette_size)
        original_image = Image.open(image_path)
        new_image = self._create_base_image()
        draw = ImageDraw.Draw(new_image)

        fonts = self._load_fonts()
        resized_original = self._resize_original_image(original_image)
        image_position = self._calculate_image_position(resized_original)

        text_positions = self._calculate_text_positions(
            draw, info, fonts, margin, image_position
        )
        self._add_text_to_image(draw, info, fonts, text_positions)

        new_image = self._paste_original_image(
            new_image, resized_original, image_position
        )

        palette_config = self._calculate_palette_config(
            palette_size, image_position, resized_original.height, margin
        )
        self._draw_color_palette(draw, palette, palette_config)

        return new_image

    def _extract_palette(self, image_path: str, palette_size: int) -> List:
        return extract_colors(image=image_path, palette_size=palette_size)

    def _create_base_image(self) -> Image.Image:
        return Image.new(
            "RGB",
            (self.dimensions.width, self.dimensions.height),
            (255, 255, 255),
        )

    def _load_fonts(
        self,
    ) -> Tuple[ImageFont.FreeTypeFont, ImageFont.FreeTypeFont]:
        font_size = 36
        return (
            ImageFont.truetype(self.font_path, font_size),
            ImageFont.truetype(self.font_path, font_size - 8),
        )

    def _resize_original_image(self, original_image: Image.Image) -> Image.Image:
        ratio = min(
            self.dimensions.width / original_image.width,
            (self.dimensions.height * 0.7) / original_image.height,
        )
        new_size = (
            int(original_image.width * ratio),
            int(original_image.height * ratio),
        )
        return original_image.resize(new_size, Resampling.LANCZOS)

    def _calculate_image_position(self, resized_original: Image.Image) -> Tuple[int, int]:
        paste_x = (self.dimensions.width - resized_original.width) // 2
        paste_y = (self.dimensions.height - resized_original.height) // 2
        return (paste_x, paste_y)

    def _calculate_text_positions(
        self,
        draw: ImageDraw.ImageDraw,
        info: ImageInfo,
        fonts: Tuple[ImageFont.FreeTypeFont, ImageFont.FreeTypeFont],
        margin: int,
        image_position: Tuple[int, int],
    ) -> dict:
        font, small_font = fonts
        camera_text_height = draw.textbbox((0, 0), info.camera, font=font)[3]
        lens_text_height = draw.textbbox((0, 0), info.lens, font=small_font)[3]

        text_y = image_position[1] - camera_text_height - lens_text_height - margin

        return {
            "camera": (margin, text_y),
            "lens": (margin, text_y + camera_text_height),
            "settings": (self.dimensions.width - margin, text_y),
        }

    def _add_text_to_image(
        self,
        draw: ImageDraw.ImageDraw,
        info: ImageInfo,
        fonts: Tuple[ImageFont.FreeTypeFont, ImageFont.FreeTypeFont],
        positions: dict,
    ):
        font, small_font = fonts
        draw.text(
            positions["camera"],
            info.camera,
            fill=(0, 0, 0),
            font=font,
            anchor="lt",
        )
        draw.text(
            positions["lens"],
            info.lens,
            fill=(0, 0, 0),
            font=small_font,
            anchor="lt",
        )
        draw.text(
            positions["settings"],
            info.settings,
            fill=(0, 0, 0),
            font=font,
            anchor="rt",
        )

    def _paste_original_image(
        self,
        new_image: Image.Image,
        resized_original: Image.Image,
        image_position: Tuple[int, int],
    ) -> Image.Image:
        new_image.paste(resized_original, image_position)
        return new_image

    def _calculate_palette_config(
        self,
        palette_size: int,
        image_position: Tuple[int, int],
        image_height: int,
        margin: int,
    ) -> dict:
        square_size = min(80, self.dimensions.width // (palette_size + 1))
        palette_width = square_size * palette_size
        return {
            "square_size": square_size,
            "start_x": (self.dimensions.width - palette_width) // 2,
            "y": image_position[1] + image_height + margin,
        }

    def _draw_color_palette(self, draw: ImageDraw.ImageDraw, palette: List, config: dict):
        for i, color in enumerate(palette):
            left = config["start_x"] + i * config["square_size"]
            top = config["y"]
            right = left + config["square_size"]
            bottom = top + config["square_size"]
            rgb_color = tuple(int(x) for x in color.rgb)
            draw.rectangle([left, top, right, bottom], fill=rgb_color)
