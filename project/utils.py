import os

from PIL import Image, ImageOps

RESOURCE_PATH = './resources'
COLLISION_RESOURCE_PATH = RESOURCE_PATH + '/collision'

GREYSCALE_BLACK = 0
GREYSCALE_WHITE = 255


def greyscale_is_black(value: int) -> bool:
    return value < 240  # matt pixel (241-255)


def is_not_black(greyscale_value: int) -> bool:
    return greyscale_value > 1


def greyscale_is_dark(value: int) -> bool:
    return value < 30


def greyscale_not_dark(value: int) -> bool:
    return value >= 100


def greyscale_not_white(value: int) -> bool:
    return value < 240


def list_resource_files(starts_with: str, ends_with: str) -> []:
    file_list = []
    for file in os.listdir(RESOURCE_PATH):
        if file.startswith(starts_with) and file.endswith(ends_with):
            file_list.append(file.replace(ends_with, ''))
    return file_list


def open_greyscale_bmp(name: str) -> Image:
    return ImageOps.grayscale(open_image(name, 'bmp'))


def open_image(name: str, file_type: str) -> Image:
    return Image.open("{}/{}.{}".format(RESOURCE_PATH, name, file_type))


def open_collision_image(hash_digest: str) -> Image:
    if collision_image_exists(hash_digest):
        return Image.open("{}/{}.bmp".format(COLLISION_RESOURCE_PATH, hash_digest))


def store_collision_image(hash_digest: str, collision_array):
    if not collision_image_exists(hash_digest):
        Image.fromarray(collision_array) \
            .convert("L") \
            .save("{}/{}.bmp".format(COLLISION_RESOURCE_PATH, hash_digest))


def collision_image_exists(hash_digest: str) -> bool:
    for file in os.listdir(COLLISION_RESOURCE_PATH):
        if file.startswith(str(hash_digest)):
            return True
    return False
