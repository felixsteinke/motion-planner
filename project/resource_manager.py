import os
from PIL import Image

RESOURCE_PATH = '../resources'
COLLISION_RESOURCE_PATH = RESOURCE_PATH + '/collision'


def resource_files(starts_with: str, ends_with: str) -> []:
    file_list = []
    for file in os.listdir(RESOURCE_PATH):
        if file.startswith(starts_with) and file.endswith(ends_with):
            file_list.append(file.replace(ends_with, ''))
    return file_list


def store_hash_image(hash_digest: str, collision_array):
    if not hash_exists(hash_digest):
        Image.fromarray(collision_array) \
            .convert("L") \
            .save(COLLISION_RESOURCE_PATH + "/%s.bmp" % hash_digest)


def load_hash_image(hash_digest: str) -> Image:
    if hash_exists(hash_digest):
        return Image.open(COLLISION_RESOURCE_PATH + "/%s.bmp" % hash_digest)


def hash_exists(hash_digest: str) -> bool:
    for file in os.listdir(COLLISION_RESOURCE_PATH):
        if file.startswith(str(hash_digest)):
            return True
    return False
