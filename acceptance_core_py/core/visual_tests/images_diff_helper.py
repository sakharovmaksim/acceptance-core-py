import logging
from pathlib import Path

from PIL import Image, ImageOps
from diffimg import diff


def get_images_diff_percent_and_save_diff_img(reference_model_local_path: Path,
                                              candidate_model_local_path: Path,
                                              diff_image_to_save_local_path: Path) -> float:
    """Return rounded diff percent from visual models and save diff image with inverted colors to local Path"""
    diff_percent = diff(str(reference_model_local_path.absolute()),
                        str(candidate_model_local_path.absolute()),
                        diff_img_file=str(diff_image_to_save_local_path.absolute()),
                        ignore_alpha=True)
    rounded_diff_percent = round(diff_percent, 2)

    image = Image.open(diff_image_to_save_local_path)
    # ImageOps.invert() working only with RGB and L images modes. Convert to RGB mode
    image = image.convert(mode='RGB')
    logging.info(f"Inverting Diff-image to {diff_image_to_save_local_path.absolute()}. Image mode {image.mode=}")
    image_inverted = ImageOps.invert(image)
    image_inverted.save(diff_image_to_save_local_path)

    return rounded_diff_percent
